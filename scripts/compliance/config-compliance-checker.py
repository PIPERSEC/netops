#!/usr/bin/env python3
"""
Network Configuration Compliance Checker

Validates network device configurations against security best practices
and organizational standards.

Author: Network Operations Team
Version: 1.0
References:
- Cisco IOS Security Best Practices: https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html
- CIS Network Device Benchmarks: https://www.cisecurity.org/cis-benchmarks/
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

try:
    from netmiko import ConnectHandler
except ImportError:
    ConnectHandler = None

class ConfigComplianceChecker:
    """Network configuration compliance checker"""

    def __init__(self, output_dir: str = "compliance_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []

        # Security best practices checks
        self.checks = {
            'cisco_ios': [
                {
                    'name': 'SSH enabled',
                    'pattern': r'ip ssh',
                    'required': True,
                    'severity': 'high'
                },
                {
                    'name': 'Telnet disabled',
                    'pattern': r'no transport input telnet',
                    'required': True,
                    'severity': 'critical'
                },
                {
                    'name': 'Password encryption',
                    'pattern': r'service password-encryption',
                    'required': True,
                    'severity': 'high'
                },
                {
                    'name': 'Login banners',
                    'pattern': r'banner (login|motd)',
                    'required': True,
                    'severity': 'medium'
                },
                {
                    'name': 'ACLs configured',
                    'pattern': r'ip access-list',
                    'required': True,
                    'severity': 'high'
                },
                {
                    'name': 'Logging configured',
                    'pattern': r'logging',
                    'required': True,
                    'severity': 'medium'
                },
                {
                    'name': 'NTP configured',
                    'pattern': r'ntp server',
                    'required': True,
                    'severity': 'medium'
                },
                {
                    'name': 'SNMP v3 only',
                    'pattern': r'snmp-server group.*v3',
                    'required': False,
                    'severity': 'high'
                }
            ]
        }

    def check_device_compliance(self, device_info: Dict, config: str = None) -> Dict:
        """Check device configuration compliance"""

        hostname = device_info.get('host')
        device_type = device_info.get('device_type')

        print(f"\n[*] Checking compliance for {hostname} ({device_type})...")

        if config is None:
            # Fetch configuration
            try:
                connection = ConnectHandler(**device_info)
                config = connection.send_command('show running-config')
                connection.disconnect()
            except Exception as e:
                print(f"    ✗ Error fetching config: {e}")
                return {'status': 'error', 'error': str(e)}

        # Run compliance checks
        compliance_results = {
            'hostname': hostname,
            'device_type': device_type,
            'timestamp': datetime.now().isoformat(),
            'checks': [],
            'score': 0,
            'max_score': 0,
            'compliance_percentage': 0
        }

        checks = self.checks.get(device_type, [])

        for check in checks:
            result = self._run_check(config, check)
            compliance_results['checks'].append(result)

            if result['passed']:
                compliance_results['score'] += result['weight']

            compliance_results['max_score'] += result['weight']

        # Calculate compliance percentage
        if compliance_results['max_score'] > 0:
            compliance_results['compliance_percentage'] = round(
                (compliance_results['score'] / compliance_results['max_score']) * 100,
                2
            )

        # Determine overall status
        if compliance_results['compliance_percentage'] >= 90:
            compliance_results['status'] = 'compliant'
            status_symbol = '✓'
        elif compliance_results['compliance_percentage'] >= 70:
            compliance_results['status'] = 'partial'
            status_symbol = '⚠'
        else:
            compliance_results['status'] = 'non-compliant'
            status_symbol = '✗'

        print(f"    [{status_symbol}] Compliance: {compliance_results['compliance_percentage']}%")
        print(f"    Score: {compliance_results['score']}/{compliance_results['max_score']}")

        # List failed checks
        failed = [c for c in compliance_results['checks'] if not c['passed']]
        if failed:
            print(f"    Failed checks ({len(failed)}):")
            for check in failed[:5]:  # Show first 5
                print(f"      - {check['name']} ({check['severity']})")

        self.results.append(compliance_results)

        return compliance_results

    def _run_check(self, config: str, check: Dict) -> Dict:
        """Run a single compliance check"""

        pattern = check['pattern']
        matches = re.findall(pattern, config, re.MULTILINE | re.IGNORECASE)

        passed = len(matches) > 0

        # Assign weight based on severity
        weight_map = {
            'critical': 10,
            'high': 5,
            'medium': 3,
            'low': 1
        }
        weight = weight_map.get(check['severity'], 1)

        return {
            'name': check['name'],
            'severity': check['severity'],
            'required': check.get('required', False),
            'passed': passed,
            'matches': len(matches),
            'weight': weight
        }

    def check_from_file(self, config_file: str, device_type: str) -> Dict:
        """Check compliance from configuration file"""

        print(f"\n[*] Checking configuration file: {config_file}")

        with open(config_file, 'r') as f:
            config = f.read()

        device_info = {
            'host': Path(config_file).stem,
            'device_type': device_type
        }

        return self.check_device_compliance(device_info, config)

    def generate_report(self) -> str:
        """Generate compliance report"""

        print(f"\n[*] Generating compliance report...")

        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_devices': len(self.results),
            'compliant': len([r for r in self.results if r['status'] == 'compliant']),
            'partial': len([r for r in self.results if r['status'] == 'partial']),
            'non_compliant': len([r for r in self.results if r['status'] == 'non-compliant']),
            'average_compliance': 0,
            'devices': self.results
        }

        if self.results:
            summary['average_compliance'] = round(
                sum(r['compliance_percentage'] for r in self.results) / len(self.results),
                2
            )

        # Save JSON report
        report_file = self.output_dir / f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"    ✓ Report saved: {report_file}")

        # Print summary
        print(f"\n{'='*70}")
        print("Configuration Compliance Summary")
        print(f"{'='*70}")
        print(f"Total Devices: {summary['total_devices']}")
        print(f"Compliant: {summary['compliant']}")
        print(f"Partial: {summary['partial']}")
        print(f"Non-Compliant: {summary['non_compliant']}")
        print(f"Average Compliance: {summary['average_compliance']}%")

        return str(report_file)


def main():
    parser = argparse.ArgumentParser(
        description='Network Configuration Compliance Checker'
    )

    parser.add_argument('--inventory', help='JSON inventory file')
    parser.add_argument('--config-file', help='Configuration file to check')
    parser.add_argument('--device-type', default='cisco_ios', help='Device type')
    parser.add_argument('--output-dir', default='compliance_reports', help='Output directory')

    args = parser.parse_args()

    if not ConnectHandler and not args.config_file:
        print("\nError: Netmiko required for live device checks")
        print("Install with: pip install netmiko")
        print("Or use --config-file to check saved configurations")
        return 1

    checker = ConfigComplianceChecker(args.output_dir)

    print("""
╔═══════════════════════════════════════════════════════════════════╗
║   Network Configuration Compliance Checker                       ║
║   Security Best Practices Validation                             ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

    if args.config_file:
        checker.check_from_file(args.config_file, args.device_type)
        checker.generate_report()
    elif args.inventory:
        with open(args.inventory, 'r') as f:
            inventory = json.load(f)

        for device in inventory.get('devices', []):
            checker.check_device_compliance(device)

        checker.generate_report()
    else:
        parser.print_help()

    return 0


if __name__ == '__main__':
    exit(main())
