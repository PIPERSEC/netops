#!/usr/bin/env python3
"""
Network Health Checker
Automated network device health and compliance checking using NAPALM.
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from napalm import get_network_driver
from typing import Dict, List

class NetworkHealthChecker:
    """Check network device health and compliance."""

    def __init__(self, inventory_file='tools/inventory/devices.yml'):
        self.inventory = self.load_inventory(inventory_file)
        self.results = []

    def load_inventory(self, filepath):
        """Load device inventory from YAML file."""
        try:
            with open(filepath) as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ Inventory file not found: {filepath}")
            return {'devices': []}

    def check_device_health(self, device_info):
        """Perform health checks on a network device."""
        hostname = device_info['hostname']
        print(f"\n🔍 Checking {hostname}...")

        health_report = {
            'hostname': hostname,
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'status': 'unknown'
        }

        try:
            # Connect to device
            driver = get_network_driver(device_info['device_type'])
            device = driver(
                hostname=hostname,
                username=device_info['username'],
                password=device_info['password'],
                optional_args=device_info.get('optional_args', {})
            )

            device.open()

            # Check 1: Device Facts
            print(f"  ✓ Connected successfully")
            facts = device.get_facts()
            health_report['checks']['facts'] = {
                'status': 'pass',
                'uptime': facts.get('uptime', 0),
                'model': facts.get('model', 'Unknown'),
                'serial': facts.get('serial_number', 'Unknown'),
                'os_version': facts.get('os_version', 'Unknown')
            }

            # Check uptime (warn if less than 1 hour - possible recent reboot)
            if facts.get('uptime', 0) < 3600:
                print(f"  ⚠️  Low uptime: {facts.get('uptime', 0)} seconds")
                health_report['checks']['uptime_warning'] = True

            # Check 2: Interface Status
            interfaces = device.get_interfaces()
            total_interfaces = len(interfaces)
            up_interfaces = sum(1 for iface in interfaces.values() if iface['is_up'])
            down_interfaces = total_interfaces - up_interfaces

            health_report['checks']['interfaces'] = {
                'total': total_interfaces,
                'up': up_interfaces,
                'down': down_interfaces,
                'status': 'pass' if down_interfaces == 0 else 'warning'
            }

            if down_interfaces > 0:
                print(f"  ⚠️  {down_interfaces} interface(s) down")
                health_report['checks']['down_interfaces'] = [
                    name for name, data in interfaces.items() if not data['is_up']
                ]

            # Check 3: BGP Neighbors (if applicable)
            try:
                bgp_neighbors = device.get_bgp_neighbors()
                if bgp_neighbors:
                    total_neighbors = sum(len(peers) for peers in bgp_neighbors.values())
                    established = sum(
                        1 for peers in bgp_neighbors.values()
                        for peer in peers.values()
                        if peer.get('is_up', False)
                    )

                    health_report['checks']['bgp'] = {
                        'total_neighbors': total_neighbors,
                        'established': established,
                        'status': 'pass' if total_neighbors == established else 'fail'
                    }

                    if total_neighbors != established:
                        print(f"  ❌ BGP: {total_neighbors - established} neighbor(s) down")
            except:
                health_report['checks']['bgp'] = {'status': 'not_configured'}

            # Check 4: Environment (Temperature, Power, Fans)
            try:
                environment = device.get_environment()

                # Check CPU
                if 'cpu' in environment:
                    for cpu_name, cpu_data in environment['cpu'].items():
                        cpu_usage = cpu_data.get('%usage', 0)
                        if cpu_usage > 80:
                            print(f"  ⚠️  High CPU usage: {cpu_usage}%")
                            health_report['checks']['high_cpu'] = cpu_usage

                # Check Memory
                if 'memory' in environment:
                    for mem_name, mem_data in environment['memory'].items():
                        mem_usage = mem_data.get('used_ram', 0) / mem_data.get('available_ram', 1) * 100
                        if mem_usage > 80:
                            print(f"  ⚠️  High memory usage: {mem_usage:.1f}%")
                            health_report['checks']['high_memory'] = mem_usage

                # Check Temperature
                if 'temperature' in environment:
                    for sensor, temp_data in environment['temperature'].items():
                        temp = temp_data.get('temperature', 0)
                        if temp > 75:
                            print(f"  ⚠️  High temperature: {sensor} = {temp}°C")
                            health_report['checks']['high_temp'] = {sensor: temp}

                health_report['checks']['environment'] = {'status': 'pass'}
            except:
                health_report['checks']['environment'] = {'status': 'not_available'}

            # Check 5: NTP Status
            try:
                ntp_stats = device.get_ntp_stats()
                if ntp_stats:
                    synced_peers = [
                        peer for peer, data in ntp_stats.items()
                        if data.get('synchronized', False)
                    ]
                    health_report['checks']['ntp'] = {
                        'status': 'pass' if synced_peers else 'fail',
                        'synced_peers': len(synced_peers)
                    }

                    if not synced_peers:
                        print(f"  ❌ NTP not synchronized")
            except:
                health_report['checks']['ntp'] = {'status': 'not_configured'}

            device.close()

            # Determine overall status
            failed_checks = [
                name for name, check in health_report['checks'].items()
                if isinstance(check, dict) and check.get('status') == 'fail'
            ]

            if failed_checks:
                health_report['status'] = 'critical'
                print(f"  ❌ Overall Status: CRITICAL")
            elif any(k.startswith('high_') or 'warning' in k for k in health_report['checks'].keys()):
                health_report['status'] = 'warning'
                print(f"  ⚠️  Overall Status: WARNING")
            else:
                health_report['status'] = 'healthy'
                print(f"  ✅ Overall Status: HEALTHY")

        except Exception as e:
            health_report['status'] = 'error'
            health_report['error'] = str(e)
            print(f"  ❌ Error: {e}")

        self.results.append(health_report)
        return health_report

    def check_all_devices(self):
        """Check health of all devices in inventory."""
        devices = self.inventory.get('devices', [])

        if not devices:
            print("❌ No devices in inventory")
            return

        print(f"Starting health checks for {len(devices)} devices...")
        print("="*80)

        for device in devices:
            self.check_device_health(device)

    def generate_summary(self):
        """Generate summary report."""
        if not self.results:
            return

        print("\n" + "="*80)
        print("Network Health Summary")
        print("="*80)

        healthy = sum(1 for r in self.results if r['status'] == 'healthy')
        warning = sum(1 for r in self.results if r['status'] == 'warning')
        critical = sum(1 for r in self.results if r['status'] == 'critical')
        error = sum(1 for r in self.results if r['status'] == 'error')

        total = len(self.results)

        print(f"\nTotal Devices: {total}")
        print(f"  ✅ Healthy: {healthy}")
        print(f"  ⚠️  Warning: {warning}")
        print(f"  ❌ Critical: {critical}")
        print(f"  🔴 Error: {error}")

        # List critical devices
        if critical > 0:
            print("\nCritical Devices:")
            for result in self.results:
                if result['status'] == 'critical':
                    print(f"  - {result['hostname']}")

        print("\n" + "="*80)

    def export_json(self, filename='network-health-report.json'):
        """Export results to JSON."""
        report = {
            'report_date': datetime.now().isoformat(),
            'total_devices': len(self.results),
            'summary': {
                'healthy': sum(1 for r in self.results if r['status'] == 'healthy'),
                'warning': sum(1 for r in self.results if r['status'] == 'warning'),
                'critical': sum(1 for r in self.results if r['status'] == 'critical'),
                'error': sum(1 for r in self.results if r['status'] == 'error'),
            },
            'devices': self.results
        }

        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Detailed report saved to {filename}")


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Network device health checker')
    parser.add_argument('--inventory', default='tools/inventory/devices.yml',
                       help='Path to inventory file')
    parser.add_argument('--export', help='Export results to JSON file')

    args = parser.parse_args()

    checker = NetworkHealthChecker(inventory_file=args.inventory)
    checker.check_all_devices()
    checker.generate_summary()

    if args.export:
        checker.export_json(args.export)


if __name__ == '__main__':
    main()
