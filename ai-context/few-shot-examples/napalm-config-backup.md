# Few-Shot Example: NAPALM Configuration Backup

## Example 1: Single Device Backup

### Input
"Create a script to backup configuration from a Cisco device using NAPALM"

### Output

**File: `scripts/backup_single_device.py`**
```python
#!/usr/bin/env python3
"""
Backup configuration from a single network device using NAPALM.
"""

import json
from datetime import datetime
from pathlib import Path
from napalm import get_network_driver

# Device configuration
DEVICE = {
    'hostname': '192.168.1.1',
    'username': 'admin',
    'password': 'cisco',  # Use environment variables in production
    'device_type': 'ios',
}

# Backup directory
BACKUP_DIR = Path('tools/backup')
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def backup_device_config(device_info):
    """
    Backup configuration from a network device.

    Args:
        device_info (dict): Device connection parameters

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Get the driver for the device type
        driver = get_network_driver(device_info['device_type'])

        # Connect to the device
        device = driver(
            hostname=device_info['hostname'],
            username=device_info['username'],
            password=device_info['password'],
        )

        print(f"Connecting to {device_info['hostname']}...")
        device.open()

        # Get the configuration
        print("Retrieving configuration...")
        config = device.get_config()

        # Get device facts for metadata
        facts = device.get_facts()

        # Close connection
        device.close()

        # Create timestamp for filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        hostname = facts['hostname']

        # Save running config
        running_config_file = BACKUP_DIR / f"{hostname}_running_{timestamp}.cfg"
        with open(running_config_file, 'w') as f:
            f.write(config['running'])

        # Save startup config
        if config.get('startup'):
            startup_config_file = BACKUP_DIR / f"{hostname}_startup_{timestamp}.cfg"
            with open(startup_config_file, 'w') as f:
                f.write(config['startup'])

        # Save device facts
        facts_file = BACKUP_DIR / f"{hostname}_facts_{timestamp}.json"
        with open(facts_file, 'w') as f:
            json.dump(facts, f, indent=2)

        print(f"✅ Backup successful for {hostname}")
        print(f"   Running config: {running_config_file}")
        if config.get('startup'):
            print(f"   Startup config: {startup_config_file}")
        print(f"   Facts: {facts_file}")

        return True, f"Backup successful for {hostname}"

    except Exception as e:
        print(f"❌ Error backing up {device_info['hostname']}: {str(e)}")
        return False, str(e)

if __name__ == '__main__':
    success, message = backup_device_config(DEVICE)
    exit(0 if success else 1)
```

## Example 2: Multi-Device Backup with Inventory

### Input
"Create a script to backup configurations from multiple devices listed in an inventory file"

### Output

**File: `scripts/backup_all_devices.py`**
```python
#!/usr/bin/env python3
"""
Backup configurations from multiple network devices using NAPALM.
Reads device inventory from YAML file.
"""

import yaml
import json
from datetime import datetime
from pathlib import Path
from napalm import get_network_driver
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

BACKUP_DIR = Path('tools/backup')
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def load_inventory(inventory_file):
    """Load device inventory from YAML file."""
    with open(inventory_file, 'r') as f:
        return yaml.safe_load(f)

def backup_device(device_info):
    """
    Backup configuration from a single device.

    Args:
        device_info (dict): Device connection parameters

    Returns:
        tuple: (hostname: str, success: bool, message: str)
    """
    hostname = device_info['hostname']

    try:
        driver = get_network_driver(device_info['device_type'])
        device = driver(
            hostname=hostname,
            username=device_info['username'],
            password=device_info['password'],
            optional_args=device_info.get('optional_args', {})
        )

        print(f"[{hostname}] Connecting...")
        device.open()

        # Get configuration and facts
        config = device.get_config()
        facts = device.get_facts()

        device.close()

        # Create timestamped backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        device_hostname = facts['hostname']

        # Save running config
        running_file = BACKUP_DIR / f"{device_hostname}_running_{timestamp}.cfg"
        running_file.write_text(config['running'])

        # Save startup config if available
        if config.get('startup'):
            startup_file = BACKUP_DIR / f"{device_hostname}_startup_{timestamp}.cfg"
            startup_file.write_text(config['startup'])

        # Save facts
        facts_file = BACKUP_DIR / f"{device_hostname}_facts_{timestamp}.json"
        facts_file.write_text(json.dumps(facts, indent=2))

        # Create latest symlinks
        latest_running = BACKUP_DIR / f"{device_hostname}_running_latest.cfg"
        latest_running.unlink(missing_ok=True)
        latest_running.symlink_to(running_file.name)

        return device_hostname, True, "Backup successful"

    except Exception as e:
        return hostname, False, str(e)

def main():
    parser = argparse.ArgumentParser(description='Backup network device configurations')
    parser.add_argument('--inventory', default='tools/inventory/devices.yml',
                       help='Path to inventory file')
    parser.add_argument('--workers', type=int, default=5,
                       help='Number of parallel workers')
    args = parser.parse_args()

    # Load inventory
    inventory = load_inventory(args.inventory)
    devices = inventory.get('devices', [])

    print(f"Starting backup for {len(devices)} devices...")
    print("=" * 60)

    # Backup devices in parallel
    results = {'success': 0, 'failed': 0, 'errors': []}

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(backup_device, dev): dev for dev in devices}

        for future in as_completed(futures):
            device = futures[future]
            hostname, success, message = future.result()

            if success:
                print(f"✅ [{hostname}] {message}")
                results['success'] += 1
            else:
                print(f"❌ [{hostname}] {message}")
                results['failed'] += 1
                results['errors'].append({'hostname': hostname, 'error': message})

    # Summary
    print("=" * 60)
    print(f"Backup Summary:")
    print(f"  Successful: {results['success']}")
    print(f"  Failed: {results['failed']}")

    if results['errors']:
        print("\nErrors:")
        for err in results['errors']:
            print(f"  - {err['hostname']}: {err['error']}")

    return 0 if results['failed'] == 0 else 1

if __name__ == '__main__':
    exit(main())
```

**File: `tools/inventory/devices.yml`**
```yaml
devices:
  - hostname: 192.168.1.1
    device_type: ios
    username: admin
    password: cisco
    optional_args:
      secret: enable_password

  - hostname: 192.168.1.2
    device_type: ios
    username: admin
    password: cisco

  - hostname: 192.168.1.10
    device_type: nxos
    username: admin
    password: cisco
    optional_args:
      port: 22

  - hostname: 192.168.1.20
    device_type: junos
    username: admin
    password: juniper
```

**Usage:**
```bash
# Backup all devices
python scripts/backup_all_devices.py

# Custom inventory file
python scripts/backup_all_devices.py --inventory inventory/production.yml

# Adjust parallelism
python scripts/backup_all_devices.py --workers 10
```
