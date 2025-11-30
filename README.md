# NetOps - Network Engineering & Automation Framework

A comprehensive framework for network engineering, automation, monitoring, and management. This repository provides standardized templates, tools, and AI-assisted workflows for building and maintaining production networks.

## Overview

This framework is designed to help network engineers:
- Automate network configuration and changes with multi-vendor support
- Maintain consistent network standards and best practices
- Leverage AI assistance with context-aware tooling
- Monitor and troubleshoot network infrastructure
- Implement network-as-code principles
- Scale network operations efficiently

## Repository Structure

```
netops/
├── projects/                    # Active network projects
├── templates/                   # Reusable automation templates
│   ├── napalm/                 # NAPALM scripts
│   ├── netmiko/                # Netmiko automation
│   ├── nornir/                 # Nornir workflows
│   ├── ansible/                # Ansible playbooks for networks
│   └── terraform/              # Network infrastructure as code
├── docs/                       # Documentation
│   ├── architecture/           # Network design docs
│   ├── runbooks/              # Operational procedures
│   ├── network-diagrams/      # Topology diagrams
│   ├── standards/             # Network standards
│   └── tutorials/             # How-to guides
├── config/                     # Configuration files
│   ├── devices/               # Device configs and templates
│   └── automation/            # Automation tool configs
├── ai-context/                 # AI assistant context
│   ├── personas/              # Network expert personas
│   ├── memory-bank/           # Persistent context
│   ├── cot-templates/         # Chain of Thought templates
│   └── few-shot-examples/     # Code examples
├── scripts/                    # Utility scripts
├── tools/                      # Network tools
│   ├── inventory/             # Network inventory
│   ├── backup/                # Config backups
│   └── monitoring/            # Monitoring scripts
└── .claude/                    # Claude Code configuration

## Getting Started

### Prerequisites

- Python 3.13+ (virtual environment included)
- Git
- SSH access to network devices
- Device credentials (stored securely)

### Installation

1. **Activate the Python virtual environment:**
   ```bash
   source bin/activate
   ```

2. **Verify network automation packages:**
   ```bash
   python -c "import napalm, netmiko, nornir; print('✅ All packages installed')"
   ```

3. **Configure device access:**
   - Store credentials securely (use Ansible Vault, environment variables, or secret manager)
   - Never commit credentials to version control

### Key Packages Installed

- **NAPALM**: Multi-vendor network automation library
- **Netmiko**: Multi-vendor SSH library for network devices
- **Nornir**: Python automation framework with inventory
- **Ansible**: Network configuration management
- **TextFSM/NTC Templates**: Parse network command output
- **Scrapli**: Fast, flexible network automation
- **ncclient**: NETCONF client library
- **Paramiko**: SSH protocol implementation

## Core Concepts

### AI Context System

#### Personas
Located in [ai-context/personas/](ai-context/personas/):
- **Network Engineer**: Core networking expertise
- **Network Automation Engineer**: Automation and programming focus
- **Network Security Engineer**: Security and compliance emphasis

#### Memory Bank
The [ai-context/memory-bank/](ai-context/memory-bank/) stores:
- Project context and current state
- Architectural decisions and network design rationale
- Best practices for network operations
- Common network issues and resolutions
- Team standards and conventions

#### Chain of Thought Templates
[ai-context/cot-templates/](ai-context/cot-templates/) provide structured approaches:
- Network design and architecture planning
- Troubleshooting methodology
- Security review and assessment

#### Few-Shot Examples
[ai-context/few-shot-examples/](ai-context/few-shot-examples/) demonstrate:
- NAPALM automation scripts
- Netmiko device interactions
- Nornir workflows
- Ansible network playbooks

### Claude Code Integration

- **Rules**: [.claude/rules.md](.claude/rules.md) defines project-specific guidelines
- **Custom Commands**: [.claude/commands/](.claude/commands/)
  - `/network-audit`: Audit network configurations
  - `/create-runbook`: Generate network runbooks
  - `/backup-configs`: Automated config backup

## Usage Examples

### 1. Automated Configuration Backup with NAPALM

```python
from napalm import get_network_driver

driver = get_network_driver('ios')
device = driver(
    hostname='192.168.1.1',
    username='admin',
    password='password'
)

device.open()
config = device.get_config()
print(config['running'])
device.close()
```

### 2. Multi-Device Config with Netmiko

```python
from netmiko import ConnectHandler

devices = [
    {'device_type': 'cisco_ios', 'host': '192.168.1.1', 'username': 'admin', 'password': 'pass'},
    {'device_type': 'cisco_ios', 'host': '192.168.1.2', 'username': 'admin', 'password': 'pass'},
]

for device in devices:
    connection = ConnectHandler(**device)
    output = connection.send_command('show version')
    print(output)
    connection.disconnect()
```

### 3. Nornir Workflow

```python
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command

nr = InitNornir(config_file="config.yaml")

result = nr.run(
    task=netmiko_send_command,
    command_string="show ip interface brief"
)

for host, task_result in result.items():
    print(f"{host}: {task_result.result}")
```

### 4. Ansible Network Playbook

```yaml
---
- name: Configure VLANs on switches
  hosts: switches
  gather_facts: no

  tasks:
    - name: Configure VLAN 10
      cisco.ios.ios_vlans:
        config:
          - vlan_id: 10
            name: DATA
            state: active
        state: merged

    - name: Save configuration
      cisco.ios.ios_config:
        save_when: always
```

## Common Tasks

### Backup Network Configurations

```bash
# Using NAPALM
python scripts/backup_configs.py

# Using Ansible
ansible-playbook playbooks/backup-configs.yml -i inventory/production
```

### Deploy Configuration Changes

```bash
# Using Nornir
python scripts/deploy_changes.py --inventory production --config vlan_config.yml

# Using Ansible
ansible-playbook playbooks/deploy-vlans.yml -i inventory/production --check
ansible-playbook playbooks/deploy-vlans.yml -i inventory/production
```

### Network Compliance Audit

```bash
# Check compliance against standards
python scripts/compliance_check.py --standard pci-dss
```

### Gather Network Inventory

```bash
# Collect device facts
ansible-playbook playbooks/gather-facts.yml -i inventory/production
```

## Best Practices

### Configuration Management
- Version control all configurations
- Use templates (Jinja2) for consistency
- Test in lab environment first
- Implement rollback procedures
- Document all changes

### Security
- Never commit credentials
- Use Ansible Vault for secrets
- Implement least privilege access
- Enable AAA and logging
- Regular security audits

### Automation
- Write idempotent scripts
- Implement error handling
- Log all automation activities
- Dry-run before applying changes
- Monitor automation job success

### Documentation
- Maintain network diagrams
- Document IP addressing schemes
- Create runbooks for operations
- Keep change logs current
- Document architectural decisions

## Network Vendor Support

### Cisco
- IOS, IOS-XE, IOS-XR, NX-OS
- ASA, Firepower
- WLC (Wireless LAN Controller)

### Juniper
- Junos (MX, EX, QFX, SRX)

### Arista
- EOS

### Palo Alto
- PAN-OS

### Others
- F5 BIG-IP
- Fortinet FortiGate
- HPE/Aruba
- Dell/Force10

## Troubleshooting

### Common Issues

See [ai-context/memory-bank/common-issues.md](ai-context/memory-bank/common-issues.md) for detailed troubleshooting.

### Quick Checks

```bash
# Test device connectivity
ping -c 4 192.168.1.1

# Test SSH access
ssh admin@192.168.1.1

# Verify Python packages
python -c "import napalm; print('NAPALM OK')"
```

## Project Organization

### Starting a New Project

```bash
mkdir -p projects/vlan-deployment
cd projects/vlan-deployment

# Create project structure
mkdir {inventory,playbooks,scripts,docs}

# Document in memory bank
# Update ai-context/memory-bank/project-context.md
```

### Using Templates

```bash
# Copy NAPALM template
cp templates/napalm/config-backup.py projects/my-project/

# Copy Ansible playbook
cp templates/ansible/configure-interfaces.yml projects/my-project/playbooks/
```

## Development Workflow

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/add-ospf-automation

# Make changes
git add .
git commit -m "feat(automation): add OSPF configuration playbook"

# Push
git push origin feature/add-ospf-automation
```

### Testing

```bash
# Test in lab environment
export NETWORK_ENV=lab
python scripts/deploy_config.py --check

# Run unit tests
pytest tests/
```

## Security Considerations

### Credential Management

**Environment Variables:**
```bash
export NETWORK_USERNAME="admin"
export NETWORK_PASSWORD="secure_password"
```

**Ansible Vault:**
```bash
# Create encrypted file
ansible-vault create inventory/group_vars/all/vault.yml

# Edit encrypted file
ansible-vault edit inventory/group_vars/all/vault.yml

# Use in playbook
ansible-playbook playbook.yml --ask-vault-pass
```

### Network Access Control

- Use jump hosts/bastion for production access
- Implement 2FA/MFA where possible
- Restrict automation system IP addresses
- Use SSH keys instead of passwords
- Rotate credentials regularly

## Monitoring & Observability

### Metrics to Monitor

- Device uptime and availability
- Interface utilization
- CPU and memory usage
- Error counters
- Spanning Tree topology changes
- BGP/OSPF neighbor states
- VPN tunnel status

### Tools Integration

- Prometheus + Grafana for metrics
- ELK Stack for log aggregation
- NetBox for IPAM and DCIM
- Oxidized for config backup

## Contributing

### Adding Templates

1. Create template in appropriate directory
2. Include README with usage instructions
3. Add examples
4. Document variables/parameters
5. Test in lab environment

### Updating Documentation

1. Keep documentation close to code
2. Update memory bank with lessons learned
3. Add runbooks for new procedures
4. Document network design changes

## Resources

### Internal Documentation
- [Network Standards](docs/standards/)
- [Runbooks](docs/runbooks/)
- [Architecture Documentation](docs/architecture/)
- [Tutorials](docs/tutorials/)

### External Resources
- [NAPALM Documentation](https://napalm.readthedocs.io/)
- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [Nornir Documentation](https://nornir.readthedocs.io/)
- [Ansible Network Automation](https://docs.ansible.com/ansible/latest/network/)
- [Network Programmability](https://developer.cisco.com/)

## License

This framework is provided for network engineering and automation work.

## Acknowledgments

Built with Claude Code for efficient AI-assisted network automation and operations.
