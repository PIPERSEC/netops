#!/usr/bin/env python3
"""
Network Device Configuration Backup Automation

Automated backup of network device configurations across multiple vendors.
Supports Cisco, Juniper, Arista, HP/HPE, and other network equipment.

Author: Network Operations Team
Version: 1.0
References:
- Netmiko: https://github.com/ktbyers/netmiko
- NAPALM: https://github.com/napalm-automation/napalm
- Best Practices: https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/15217-copy-configs-snmp.html
"""

import argparse
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import difflib

try:
    from netmiko import ConnectHandler
    from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
except ImportError:
    print("⚠ Netmiko not installed. Install with: pip install netmiko")
    ConnectHandler = None

class NetworkDeviceBackup:
    """Automated network device configuration backup"""

    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger('NetworkBackup')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(self.backup_dir / 'backup.log')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)

        self.results = {
            'timestamp': datetime.now().isoformat(),
            'devices_backed_up': 0,
            'devices_failed': 0,
            'changes_detected': 0,
            'backups': []
        }

    def backup_device(self, device_info: Dict) -> Dict:
        """
        Backup configuration from a single network device

        Args:
            device_info: Dictionary with device connection parameters
                {
                    'device_type': 'cisco_ios',
                    'host': '192.168.1.1',
                    'username': 'admin',
                    'password': 'password',
                    'secret': 'enable_password',  # Optional
                    'port': 22  # Optional
                }
        """
        hostname = device_info.get('host')
        device_type = device_info.get('device_type')

        print(f"\n[*] Backing up {hostname} ({device_type})...")
        self.logger.info(f"Starting backup for {hostname}")

        try:
            # Connect to device
            connection = ConnectHandler(**device_info)

            # Get hostname from device
            if device_type.startswith('cisco'):
                actual_hostname = connection.find_prompt().strip('#>')
            else:
                actual_hostname = hostname.replace('.', '_')

            # Get configuration based on device type
            config = self._get_configuration(connection, device_type)

            # Save backup
            backup_result = self._save_backup(actual_hostname, config)

            # Disconnect
            connection.disconnect()

            print(f"    ✓ Backup completed: {backup_result['filename']}")
            if backup_result['changed']:
                print(f"    ⚠ Configuration changed since last backup")

            self.results['devices_backed_up'] += 1
            if backup_result['changed']:
                self.results['changes_detected'] += 1

            self.results['backups'].append({
                'hostname': actual_hostname,
                'ip': hostname,
                'device_type': device_type,
                'status': 'success',
                'filename': backup_result['filename'],
                'changed': backup_result['changed'],
                'size': backup_result['size']
            })

            return {'status': 'success', 'result': backup_result}

        except NetmikoTimeoutException:
            error = f"Connection timeout to {hostname}"
            print(f"    ✗ {error}")
            self.logger.error(error)
            self.results['devices_failed'] += 1
            return {'status': 'failed', 'error': error}

        except NetmikoAuthenticationException:
            error = f"Authentication failed for {hostname}"
            print(f"    ✗ {error}")
            self.logger.error(error)
            self.results['devices_failed'] += 1
            return {'status': 'failed', 'error': error}

        except Exception as e:
            error = f"Error backing up {hostname}: {str(e)}"
            print(f"    ✗ {error}")
            self.logger.error(error)
            self.results['devices_failed'] += 1
            return {'status': 'failed', 'error': error}

    def _get_configuration(self, connection, device_type: str) -> str:
        """Get configuration based on device type"""

        commands = {
            'cisco_ios': 'show running-config',
            'cisco_nxos': 'show running-config',
            'cisco_asa': 'show running-config',
            'cisco_xr': 'show running-config',
            'arista_eos': 'show running-config',
            'juniper': 'show configuration | display set',
            'juniper_junos': 'show configuration | display set',
            'hp_comware': 'display current-configuration',
            'hp_procurve': 'show running-config',
            'dell_force10': 'show running-config',
            'paloalto_panos': 'show config running',
        }

        command = commands.get(device_type, 'show running-config')

        # Send command
        output = connection.send_command(command, delay_factor=2)

        return output

    def _save_backup(self, hostname: str, config: str) -> Dict:
        """Save backup and detect changes"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create device directory
        device_dir = self.backup_dir / hostname
        device_dir.mkdir(exist_ok=True)

        # Current backup filename
        current_file = device_dir / f"{hostname}_{timestamp}.cfg"

        # Save current backup
        with open(current_file, 'w') as f:
            f.write(config)

        # Create/update latest symlink
        latest_link = device_dir / f"{hostname}_latest.cfg"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(current_file.name)

        # Check for changes
        changed = False
        previous_files = sorted(device_dir.glob(f"{hostname}_*.cfg"))

        if len(previous_files) > 1:
            # Compare with previous backup
            previous_file = previous_files[-2]

            with open(previous_file, 'r') as f:
                previous_config = f.read()

            if config != previous_config:
                changed = True

                # Generate diff
                diff_file = device_dir / f"{hostname}_{timestamp}.diff"
                diff = difflib.unified_diff(
                    previous_config.splitlines(keepends=True),
                    config.splitlines(keepends=True),
                    fromfile=str(previous_file),
                    tofile=str(current_file)
                )

                with open(diff_file, 'w') as f:
                    f.writelines(diff)

        return {
            'filename': str(current_file),
            'changed': changed,
            'size': current_file.stat().st_size
        }

    def backup_from_inventory(self, inventory_file: str):
        """Backup all devices from inventory file"""

        print(f"\n[*] Loading inventory from {inventory_file}...")

        with open(inventory_file, 'r') as f:
            inventory = json.load(f)

        devices = inventory.get('devices', [])
        print(f"    Found {len(devices)} device(s) in inventory")

        for device in devices:
            self.backup_device(device)

        # Generate summary report
        self._generate_report()

    def _generate_report(self):
        """Generate backup summary report"""

        print(f"\n{'='*70}")
        print("Backup Summary")
        print(f"{'='*70}")
        print(f"Devices backed up: {self.results['devices_backed_up']}")
        print(f"Devices failed: {self.results['devices_failed']}")
        print(f"Changes detected: {self.results['changes_detected']}")

        # Save JSON report
        report_file = self.backup_dir / f"backup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\nReport saved: {report_file}")

        # List changed devices
        if self.results['changes_detected'] > 0:
            print(f"\nDevices with configuration changes:")
            for backup in self.results['backups']:
                if backup['changed']:
                    print(f"  - {backup['hostname']} ({backup['ip']})")


def main():
    parser = argparse.ArgumentParser(
        description='Network Device Configuration Backup Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Backup from inventory file
  python network-device-backup.py --inventory devices.json

  # Backup single device
  python network-device-backup.py --host 192.168.1.1 --type cisco_ios --user admin

Sample inventory.json:
{
  "devices": [
    {
      "device_type": "cisco_ios",
      "host": "192.168.1.1",
      "username": "admin",
      "password": "password"
    },
    {
      "device_type": "juniper_junos",
      "host": "192.168.1.2",
      "username": "admin",
      "password": "password"
    }
  ]
}
        """
    )

    parser.add_argument('--inventory', help='JSON inventory file with device list')
    parser.add_argument('--host', help='Single device IP address')
    parser.add_argument('--type', help='Device type (cisco_ios, juniper_junos, etc.)')
    parser.add_argument('--user', help='Username')
    parser.add_argument('--password', help='Password')
    parser.add_argument('--backup-dir', default='backups', help='Backup directory')

    args = parser.parse_args()

    if not ConnectHandler:
        print("\nError: Netmiko is required but not installed.")
        print("Install with: pip install netmiko")
        return 1

    backup = NetworkDeviceBackup(args.backup_dir)

    print("""
╔═══════════════════════════════════════════════════════════════════╗
║   Network Device Configuration Backup                            ║
║   Multi-Vendor Support via Netmiko                               ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

    if args.inventory:
        backup.backup_from_inventory(args.inventory)
    elif args.host and args.type:
        device_info = {
            'device_type': args.type,
            'host': args.host,
            'username': args.user or input("Username: "),
            'password': args.password or input("Password: ")
        }
        backup.backup_device(device_info)
        backup._generate_report()
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
