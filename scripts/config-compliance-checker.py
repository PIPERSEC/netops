#!/usr/bin/env python3
"""
Network Configuration Compliance Checker
Validates network device configurations against security and operational standards.
"""

import re
import yaml
from napalm import get_network_driver
from typing import Dict, List

class ConfigComplianceChecker:
    """Check network configurations for compliance."""

    def __init__(self):
        self.compliance_rules = self.load_compliance_rules()
        self.results = []

    def load_compliance_rules(self):
        """Load compliance rules."""
        return {
            'cisco_ios': [
                {
                    'name': 'No IP Source Routing',
                    'check': lambda config: 'no ip source-route' in config,
                    'severity': 'high',
                    'description': 'IP source routing should be disabled'
                },
                {
                    'name': 'Service Password Encryption',
                    'check': lambda config: 'service password-encryption' in config,
                    'severity': 'high',
                    'description': 'Password encryption should be enabled'
                },
                {
                    'name': 'Enable Secret Configured',
                    'check': lambda config: 'enable secret' in config,
                    'severity': 'critical',
                    'description': 'Enable secret must be configured'
                },
                {
                    'name': 'AAA Authentication',
                    'check': lambda config: 'aaa new-model' in config,
                    'severity': 'high',
                    'description': 'AAA should be configured for authentication'
                },
                {
                    'name': 'Logging Enabled',
                    'check': lambda config: re.search(r'logging \d+\.\d+\.\d+\.\d+', config),
                    'severity': 'medium',
                    'description': 'Centralized logging should be configured'
                },
                {
                    'name': 'NTP Configured',
                    'check': lambda config: 'ntp server' in config,
                    'severity': 'medium',
                    'description': 'NTP should be configured for accurate time'
                },
                {
                    'name': 'SNMP Community Not Public',
                    'check': lambda config: 'snmp-server community public' not in config.lower(),
                    'severity': 'critical',
                    'description': 'Default SNMP community should not be used'
                },
                {
                    'name': 'SSH Configured',
                    'check': lambda config: 'transport input ssh' in config or 'ip ssh' in config,
                    'severity': 'high',
                    'description': 'SSH should be configured and Telnet disabled'
                },
                {
                    'name': 'No Telnet',
                    'check': lambda config: 'transport input telnet' not in config,
                    'severity': 'high',
                    'description': 'Telnet should be disabled'
                },
                {
                    'name': 'Banner Configured',
                    'check': lambda config: 'banner' in config,
                    'severity': 'low',
                    'description': 'Login banner should be configured'
                },
            ],
            'junos': [
                {
                    'name': 'Root Authentication',
                    'check': lambda config: 'root-authentication' in config,
                    'severity': 'critical',
                    'description': 'Root authentication must be configured'
                },
                {
                    'name': 'SSH Service Enabled',
                    'check': lambda config: 'system services ssh' in config,
                    'severity': 'high',
                    'description': 'SSH service should be enabled'
                },
                {
                    'name': 'NTP Configured',
                    'check': lambda config: 'system ntp' in config,
                    'severity': 'medium',
                    'description': 'NTP should be configured'
                },
                {
                    'name': 'Syslog Configured',
                    'check': lambda config: 'system syslog' in config,
                    'severity': 'medium',
                    'description': 'Syslog should be configured'
                },
            ]
        }

    def check_device_compliance(self, device_info):
        """Check a device for compliance."""
        hostname = device_info['hostname']
        device_type = device_info['device_type']

        print(f"\n🔍 Checking compliance for {hostname} ({device_type})...")

        compliance_report = {
            'hostname': hostname,
            'device_type': device_type,
            'passed': [],
            'failed': [],
            'not_applicable': []
        }

        try:
            # Connect to device
            driver = get_network_driver(device_type)
            device = driver(
                hostname=hostname,
                username=device_info['username'],
                password=device_info['password']
            )

            device.open()

            # Get configuration
            config = device.get_config()
            running_config = config['running']

            device.close()

            # Get rules for this device type
            rules = self.compliance_rules.get(device_type, [])

            if not rules:
                print(f"  ⚠️  No compliance rules defined for {device_type}")
                compliance_report['not_applicable'].append(
                    f'No rules for device type {device_type}'
                )
                self.results.append(compliance_report)
                return compliance_report

            # Check each rule
            for rule in rules:
                try:
                    if rule['check'](running_config):
                        compliance_report['passed'].append(rule['name'])
                        print(f"  ✅ {rule['name']}")
                    else:
                        compliance_report['failed'].append({
                            'rule': rule['name'],
                            'severity': rule['severity'],
                            'description': rule['description']
                        })
                        print(f"  ❌ {rule['name']} - {rule['severity'].upper()}")
                except Exception as e:
                    print(f"  ⚠️  Could not check {rule['name']}: {e}")

            # Summary for this device
            total = len(rules)
            passed = len(compliance_report['passed'])
            failed = len(compliance_report['failed'])

            print(f"\n  Compliance Score: {passed}/{total} ({(passed/total*100):.1f}%)")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            compliance_report['error'] = str(e)

        self.results.append(compliance_report)
        return compliance_report

    def check_all_devices(self, inventory_file='tools/inventory/devices.yml'):
        """Check all devices in inventory."""
        try:
            with open(inventory_file) as f:
                inventory = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ Inventory file not found: {inventory_file}")
            return

        devices = inventory.get('devices', [])

        if not devices:
            print("❌ No devices in inventory")
            return

        print(f"Checking compliance for {len(devices)} devices...")
        print("="*80)

        for device in devices:
            self.check_device_compliance(device)

    def generate_summary(self):
        """Generate compliance summary report."""
        if not self.results:
            return

        print("\n" + "="*80)
        print("Network Compliance Summary")
        print("="*80)

        total_devices = len(self.results)
        fully_compliant = sum(1 for r in self.results if len(r.get('failed', [])) == 0 and len(r.get('passed', [])) > 0)

        print(f"\nTotal Devices Checked: {total_devices}")
        print(f"Fully Compliant: {fully_compliant}")
        print(f"Non-Compliant: {total_devices - fully_compliant}")

        # Critical failures
        critical_failures = []
        for result in self.results:
            for failure in result.get('failed', []):
                if isinstance(failure, dict) and failure.get('severity') == 'critical':
                    critical_failures.append({
                        'hostname': result['hostname'],
                        'rule': failure['rule']
                    })

        if critical_failures:
            print(f"\n❌ Critical Compliance Failures: {len(critical_failures)}")
            for failure in critical_failures:
                print(f"  - {failure['hostname']}: {failure['rule']}")

        print("\n" + "="*80)


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Network configuration compliance checker')
    parser.add_argument('--inventory', default='tools/inventory/devices.yml',
                       help='Path to inventory file')

    args = parser.parse_args()

    checker = ConfigComplianceChecker()
    checker.check_all_devices(inventory_file=args.inventory)
    checker.generate_summary()


if __name__ == '__main__':
    main()
