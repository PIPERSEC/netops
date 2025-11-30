# NetOps Framework - Quick Start Guide

Welcome to your comprehensive Network Engineering & Automation framework!

## What You Have

A complete, production-ready framework for network operations with:

### 🤖 AI-Assisted Network Operations
- **Personas**: Network Engineer, Network Automation Engineer, Network Security Engineer
- **Memory Bank**: Persistent context for network projects and decisions
- **Chain of Thought Templates**: Structured approaches for network design and troubleshooting
- **Few-Shot Examples**: Network automation code patterns

### 🛠️ Network Automation Tools
- **NAPALM**: Multi-vendor network automation library
- **Netmiko**: SSH library for network devices
- **Nornir**: Python automation framework
- **Ansible**: Network configuration management
- **TextFSM**: Parse network device output
- **Scrapli**: Fast network automation

### 📚 Documentation & Standards
- Comprehensive README
- Network automation best practices
- Security guidelines
- Configuration management standards

## Quick Start (3 Steps)

### 1. Activate Environment

```bash
cd /Users/jcox/Repos/Default/envs/netops
source bin/activate
```

### 2. Verify Installation

```bash
# Check installed packages
python -c "import napalm, netmiko, nornir; print('✅ All packages ready!')"

# List all network packages
pip list | grep -E "(napalm|netmiko|nornir|ansible|scrapli)"
```

### 3. Try Your First Automation

**Simple Device Connection Test:**

```python
from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
}

connection = ConnectHandler(**device)
output = connection.send_command('show version')
print(output)
connection.disconnect()
```

## Directory Overview

```
netops/
├── projects/              # Your network automation projects
├── templates/             # Reusable automation templates
│   ├── napalm/           # NAPALM scripts
│   ├── netmiko/          # Netmiko scripts
│   ├── nornir/           # Nornir workflows
│   └── ansible/          # Network playbooks
├── ai-context/           # AI assistance context
│   ├── personas/         # Network expert personas
│   ├── memory-bank/      # Persistent knowledge
│   └── few-shot-examples/# Code examples
├── tools/
│   ├── inventory/        # Device inventories
│   ├── backup/           # Config backups
│   └── monitoring/       # Monitoring scripts
└── docs/                 # Documentation
```

## Common Network Tasks

### 1. Backup Device Configurations

**Using NAPALM:**
```python
from napalm import get_network_driver

driver = get_network_driver('ios')
device = driver(hostname='192.168.1.1', username='admin', password='pass')

device.open()
config = device.get_config()
print(config['running'])
device.close()
```

### 2. Deploy Configuration Changes

**Using Netmiko:**
```python
from netmiko import ConnectHandler

device = ConnectHandler(
    device_type='cisco_ios',
    host='192.168.1.1',
    username='admin',
    password='password'
)

commands = [
    'interface GigabitEthernet0/1',
    'description Configured by automation',
    'no shutdown'
]

output = device.send_config_set(commands)
device.save_config()
print(output)
```

### 3. Multi-Device Operations

**Using Nornir:**
```python
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command

nr = InitNornir(config_file="config.yaml")

result = nr.run(
    task=netmiko_send_command,
    command_string="show ip interface brief"
)

for host, task_result in result.items():
    print(f"\n{host}:\n{task_result.result}")
```

## AI Context Usage

### Before Starting Work:
1. Review `ai-context/personas/network-engineer.md` for networking mindset
2. Check `ai-context/memory-bank/best-practices.md` for network automation patterns
3. Use `ai-context/cot-templates/` for structured network design decisions

### Claude Code Integration:
```
/network-audit          # Audit network configurations
/create-runbook         # Generate network runbooks
/backup-configs         # Automated backup procedures
```

## Security Best Practices

✅ **Never commit credentials** - Use environment variables or vaults
✅ **Use SSH keys** instead of passwords
✅ **Enable device logging** - Track all automation activities
✅ **Test in lab first** - Never test directly in production
✅ **Implement rollback** - Always have a back-out plan
✅ **Monitor changes** - Watch for unexpected impacts

## Network Vendor Support

- ✅ Cisco (IOS, IOS-XE, IOS-XR, NX-OS, ASA)
- ✅ Juniper (Junos)
- ✅ Arista (EOS)
- ✅ Palo Alto (PAN-OS)
- ✅ Fortinet (FortiGate)
- ✅ F5 (BIG-IP)
- ✅ HPE/Aruba

## Example Projects

### Project 1: Configuration Backup System
```bash
mkdir -p projects/config-backup
cd projects/config-backup

# Copy template
cp ../../ai-context/few-shot-examples/napalm-config-backup.md reference.md

# Create your script
# Implement automated daily backups
```

### Project 2: VLAN Deployment Automation
```bash
mkdir -p projects/vlan-automation
cd projects/vlan-automation

# Use Ansible for network-wide VLAN deployment
```

### Project 3: Network Compliance Auditing
```bash
mkdir -p projects/compliance-audit
cd projects/compliance-audit

# Check devices against security baselines
```

## Troubleshooting

### Can't connect to devices?
```bash
# Test connectivity
ping 192.168.1.1

# Test SSH access
ssh admin@192.168.1.1

# Check credentials (use environment variables)
export NET_USERNAME="admin"
export NET_PASSWORD="password"
```

### Package import errors?
```bash
# Ensure virtual environment is activated
source bin/activate

# Reinstall if needed
pip install napalm netmiko nornir
```

## Next Steps

- [ ] Configure your device inventory in `tools/inventory/`
- [ ] Set up credentials securely (Ansible Vault or environment variables)
- [ ] Create your first automation project
- [ ] Document network topology in `docs/network-diagrams/`
- [ ] Set up automated configuration backups
- [ ] Implement compliance checking
- [ ] Create network runbooks

## Resources

- **Framework Docs**: [README.md](README.md)
- **AI Context**: [ai-context/memory-bank/](ai-context/memory-bank/)
- **Examples**: [ai-context/few-shot-examples/](ai-context/few-shot-examples/)
- **NAPALM Docs**: https://napalm.readthedocs.io/
- **Netmiko Docs**: https://github.com/ktbyers/netmiko
- **Nornir Docs**: https://nornir.readthedocs.io/

## Getting Help

1. Check [ai-context/memory-bank/common-issues.md](ai-context/memory-bank/common-issues.md)
2. Review [docs/tutorials/](docs/tutorials/) for guides
3. Use Claude Code commands for assistance
4. Consult vendor-specific documentation

**Happy network automating! 🚀**

---

**Version**: 1.0.0
**Created**: 2025-11-30
**Repository**: https://github.com/PIPERSEC/netops
