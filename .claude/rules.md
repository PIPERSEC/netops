# Claude Rules for NetOps Projects

## Context Awareness
- Always review relevant files in `ai-context/memory-bank/` before starting work
- Check `ai-context/personas/` to understand the required network expertise level
- Consult `ai-context/cot-templates/` for structured thinking approaches
- Reference `ai-context/few-shot-examples/` for network automation patterns

## Network Engineering Principles
1. **Network Stability First**: Prioritize network uptime and stability
2. **Change Control**: Test in lab before production
3. **Rollback Plans**: Always have a rollback procedure
4. **Documentation**: Document network changes and topology
5. **Security by Default**: Apply security best practices from the start
6. **Automation**: Automate repetitive network tasks
7. **Multi-Vendor Support**: Design for vendor diversity

## Code Standards
- Follow Python PEP 8 for network automation scripts
- Use environment variables or vaults for credentials
- Implement proper error handling and retries
- Log all network changes and automation activities
- Use meaningful variable and function names
- Add docstrings for network automation functions

## Network Automation Requirements
- **Idempotency**: Scripts should be safe to run multiple times
- **Dry-Run Mode**: Implement check/dry-run before applying changes
- **Vendor Abstraction**: Use NAPALM when possible for multi-vendor support
- **Connection Management**: Properly open and close device connections
- **Timeout Handling**: Set appropriate timeouts for network operations
- **Credential Security**: Never commit credentials to version control

## Documentation Requirements
- Update architectural decisions in `ai-context/memory-bank/architectural-decisions.md`
- Document network automation patterns in `ai-context/memory-bank/best-practices.md`
- Add troubleshooting steps to `ai-context/memory-bank/common-issues.md`
- Keep project context current in `ai-context/memory-bank/project-context.md`
- Maintain network diagrams in `docs/network-diagrams/`
- Create runbooks for network operations

## Security Requirements
- Never commit device credentials or secrets
- Use Ansible Vault, environment variables, or secret managers
- Implement least privilege access for automation accounts
- Enable AAA logging on network devices
- Use SSH keys instead of passwords where possible
- Encrypt sensitive network data
- Document security decisions and considerations

## Testing and Validation
- Test automation scripts in lab environment first
- Implement configuration validation before deployment
- Use --check mode in Ansible playbooks
- Verify network connectivity after changes
- Monitor network metrics during and after changes
- Implement automated compliance checking

## Network Change Management
- Follow change control procedures
- Schedule changes during maintenance windows
- Notify stakeholders before network changes
- Document pre-change and post-change states
- Keep rollback configurations ready
- Monitor for issues after changes

## Git Workflow
- Use descriptive commit messages following conventional commits
- Create feature branches for network automation projects
- Require code review for production network changes
- Tag releases appropriately
- Keep commit history clean and logical

## Operational Excellence
- Implement comprehensive network monitoring
- Create runbooks for common network operations
- Plan for network disaster recovery
- Document on-call procedures for network incidents
- Conduct post-mortems for network outages
- Continuously improve network automation

## When Working on Network Projects
1. Review existing network context in memory bank
2. Select appropriate persona (Network Engineer, Automation Engineer, Security Engineer)
3. Use Chain of Thought templates for complex network decisions
4. Follow few-shot examples for consistency in automation scripts
5. Update documentation as you work
6. Test thoroughly in lab before production deployment
7. Update memory bank with lessons learned

## Network-Specific Best Practices
- Maintain accurate network topology diagrams
- Keep IP address management (IPAM) current
- Document VLAN assignments and purposes
- Track network device inventory
- Version control all network configurations
- Backup configurations before changes
- Use configuration templates for consistency
