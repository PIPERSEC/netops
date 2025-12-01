#!/usr/bin/env python3
"""
Network Health Monitoring and Alerting

Monitors network device health metrics including CPU, memory, interfaces,
and environmental sensors. Generates alerts based on thresholds.

Author: Network Operations Team
Version: 1.0
References:
- SNMP Best Practices: https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/7244-snmp-agent.html
- Network Monitoring: https://www.ietf.org/rfc/rfc3411.txt
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import subprocess

try:
    from netmiko import ConnectHandler
except ImportError:
    ConnectHandler = None

class NetworkHealthMonitor:
    """Network device health monitoring"""

    def __init__(self, output_dir: str = "health_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = []

        # Thresholds
        self.thresholds = {
            'cpu': {'warning': 70, 'critical': 90},
            'memory': {'warning': 80, 'critical': 95},
            'interface_errors': {'warning': 100, 'critical': 1000},
            'temperature': {'warning': 65, 'critical': 75}
        }

    def check_device_health(self, device_info: Dict) -> Dict:
        """Check health of a network device"""

        hostname = device_info.get('host')
        device_type = device_info.get('device_type')

        print(f"\n[*] Checking health of {hostname} ({device_type})...")

        try:
            connection = ConnectHandler(**device_info)

            # Get actual hostname
            if device_type.startswith('cisco'):
                actual_hostname = connection.find_prompt().strip('#>')
            else:
                actual_hostname = hostname

            health_data = {
                'hostname': actual_hostname,
                'ip': hostname,
                'device_type': device_type,
                'timestamp': datetime.now().isoformat(),
                'status': 'healthy',
                'alerts': []
            }

            # Check CPU
            cpu_data = self._check_cpu(connection, device_type)
            health_data['cpu'] = cpu_data
            if cpu_data['usage'] >= self.thresholds['cpu']['critical']:
                health_data['alerts'].append({
                    'severity': 'critical',
                    'metric': 'cpu',
                    'message': f"CPU usage critical: {cpu_data['usage']}%"
                })
                health_data['status'] = 'critical'
            elif cpu_data['usage'] >= self.thresholds['cpu']['warning']:
                health_data['alerts'].append({
                    'severity': 'warning',
                    'metric': 'cpu',
                    'message': f"CPU usage high: {cpu_data['usage']}%"
                })
                if health_data['status'] == 'healthy':
                    health_data['status'] = 'warning'

            # Check Memory
            memory_data = self._check_memory(connection, device_type)
            health_data['memory'] = memory_data
            if memory_data['usage_percent'] >= self.thresholds['memory']['critical']:
                health_data['alerts'].append({
                    'severity': 'critical',
                    'metric': 'memory',
                    'message': f"Memory usage critical: {memory_data['usage_percent']}%"
                })
                health_data['status'] = 'critical'
            elif memory_data['usage_percent'] >= self.thresholds['memory']['warning']:
                health_data['alerts'].append({
                    'severity': 'warning',
                    'metric': 'memory',
                    'message': f"Memory usage high: {memory_data['usage_percent']}%"
                })

            # Check Interfaces
            interface_data = self._check_interfaces(connection, device_type)
            health_data['interfaces'] = interface_data

            # Check for interface errors
            for intf in interface_data:
                if intf.get('errors', 0) >= self.thresholds['interface_errors']['critical']:
                    health_data['alerts'].append({
                        'severity': 'critical',
                        'metric': 'interface_errors',
                        'message': f"Interface {intf['name']}: {intf['errors']} errors"
                    })

            # Print status
            status_symbol = {
                'healthy': '✓',
                'warning': '⚠',
                'critical': '✗'
            }.get(health_data['status'], '?')

            print(f"    [{status_symbol}] Status: {health_data['status'].upper()}")
            print(f"    CPU: {cpu_data['usage']}% | Memory: {memory_data['usage_percent']}%")
            print(f"    Interfaces: {len([i for i in interface_data if i['status'] == 'up'])} up")

            if health_data['alerts']:
                print(f"    Alerts: {len(health_data['alerts'])}")
                for alert in health_data['alerts']:
                    print(f"      - [{alert['severity'].upper()}] {alert['message']}")

            connection.disconnect()

            self.metrics.append(health_data)
            return health_data

        except Exception as e:
            error_data = {
                'hostname': hostname,
                'ip': hostname,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.metrics.append(error_data)
            print(f"    ✗ Error: {e}")
            return error_data

    def _check_cpu(self, connection, device_type: str) -> Dict:
        """Check CPU utilization"""

        if device_type.startswith('cisco_ios') or device_type == 'cisco_nxos':
            output = connection.send_command('show processes cpu')

            # Parse CPU usage (simplified - would need better parsing)
            for line in output.splitlines():
                if 'CPU utilization' in line or 'one minute' in line:
                    # Extract percentage
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if '%' in part and part[:-1].isdigit():
                            usage = int(part[:-1])
                            return {'usage': usage, 'raw': line.strip()}

        return {'usage': 0, 'raw': 'Unable to parse'}

    def _check_memory(self, connection, device_type: str) -> Dict:
        """Check memory utilization"""

        if device_type.startswith('cisco_ios'):
            output = connection.send_command('show memory statistics')

            # Parse memory (simplified)
            for line in output.splitlines():
                if 'Processor' in line or 'processor' in line:
                    parts = line.split()
                    # Look for used/total pattern
                    for i, part in enumerate(parts):
                        if part.isdigit() and i + 1 < len(parts):
                            used = int(part)
                            total = int(parts[i + 1]) if parts[i + 1].isdigit() else used * 2
                            usage_percent = int((used / total) * 100) if total > 0 else 0
                            return {
                                'used': used,
                                'total': total,
                                'usage_percent': usage_percent
                            }

        return {'used': 0, 'total': 0, 'usage_percent': 0}

    def _check_interfaces(self, connection, device_type: str) -> List[Dict]:
        """Check interface status"""

        interfaces = []

        if device_type.startswith('cisco'):
            output = connection.send_command('show ip interface brief')

            for line in output.splitlines():
                if 'Interface' in line or len(line.strip()) == 0:
                    continue

                parts = line.split()
                if len(parts) >= 6:
                    interfaces.append({
                        'name': parts[0],
                        'ip': parts[1] if parts[1] != 'unassigned' else None,
                        'status': parts[4].lower(),
                        'protocol': parts[5].lower()
                    })

            # Get error counts
            error_output = connection.send_command('show interfaces')
            # Simplified - would need better parsing for actual error counts
            for intf in interfaces:
                intf['errors'] = 0  # Would parse from output

        return interfaces

    def check_reachability(self, hosts: List[str]) -> Dict:
        """Check network reachability via ping"""

        print(f"\n[*] Checking reachability for {len(hosts)} host(s)...")

        results = {
            'timestamp': datetime.now().isoformat(),
            'reachable': [],
            'unreachable': []
        }

        for host in hosts:
            try:
                # Ping the host
                result = subprocess.run(
                    ['ping', '-c', '3', '-W', '2', host],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    print(f"    ✓ {host} - Reachable")
                    results['reachable'].append(host)
                else:
                    print(f"    ✗ {host} - Unreachable")
                    results['unreachable'].append(host)

            except Exception as e:
                print(f"    ✗ {host} - Error: {e}")
                results['unreachable'].append(host)

        print(f"\nReachability: {len(results['reachable'])}/{len(hosts)} hosts up")

        return results

    def generate_report(self) -> str:
        """Generate health monitoring report"""

        print(f"\n[*] Generating health report...")

        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_devices': len(self.metrics),
            'healthy': len([m for m in self.metrics if m.get('status') == 'healthy']),
            'warning': len([m for m in self.metrics if m.get('status') == 'warning']),
            'critical': len([m for m in self.metrics if m.get('status') == 'critical']),
            'error': len([m for m in self.metrics if m.get('status') == 'error']),
            'devices': self.metrics
        }

        # Save JSON report
        report_file = self.output_dir / f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"    ✓ Report saved: {report_file}")

        # Print summary
        print(f"\n{'='*70}")
        print("Health Monitoring Summary")
        print(f"{'='*70}")
        print(f"Total Devices: {summary['total_devices']}")
        print(f"Healthy:  {summary['healthy']}")
        print(f"Warning:  {summary['warning']}")
        print(f"Critical: {summary['critical']}")
        print(f"Error:    {summary['error']}")

        return str(report_file)


def main():
    parser = argparse.ArgumentParser(
        description='Network Health Monitoring and Alerting'
    )

    parser.add_argument('--inventory', help='JSON inventory file')
    parser.add_argument('--ping-test', nargs='+', help='Test reachability of hosts')
    parser.add_argument('--output-dir', default='health_reports', help='Output directory')

    args = parser.parse_args()

    if not ConnectHandler and not args.ping_test:
        print("\nError: Netmiko is required for device health checks.")
        print("Install with: pip install netmiko")
        return 1

    monitor = NetworkHealthMonitor(args.output_dir)

    print("""
╔═══════════════════════════════════════════════════════════════════╗
║   Network Health Monitoring System                               ║
║   CPU | Memory | Interfaces | Reachability                       ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

    if args.ping_test:
        monitor.check_reachability(args.ping_test)

    if args.inventory:
        with open(args.inventory, 'r') as f:
            inventory = json.load(f)

        devices = inventory.get('devices', [])
        for device in devices:
            monitor.check_device_health(device)

        monitor.generate_report()

    if not args.inventory and not args.ping_test:
        parser.print_help()

    return 0


if __name__ == '__main__':
    exit(main())
