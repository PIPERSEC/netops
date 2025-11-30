# Team Preferences and Standards

## Coding Standards

### Python
- Follow PEP 8 style guide
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for functions and classes
- Prefer f-strings for formatting
- Use virtual environments
- Requirements in `requirements.txt` and `requirements-dev.txt`

### Shell Scripts
- Use `#!/bin/bash` shebang
- Enable strict mode: `set -euo pipefail`
- Use meaningful variable names (UPPER_CASE for constants)
- Include usage/help function
- Comment complex logic
- Handle errors explicitly

### YAML
- Use 2 spaces for indentation
- Quote strings when ambiguous
- Use `---` document separator
- Organize logically (metadata, spec, status)

## Infrastructure as Code

### Terraform
- Use workspaces for environment separation
- Implement remote state with locking
- Use modules for reusable components
- Variables in `variables.tf`, outputs in `outputs.tf`
- Use `terraform fmt` before committing
- Include `README.md` in each module
- Use semantic versioning for modules

### Ansible
- Use roles for organization
- Variables in `group_vars` and `host_vars`
- Sensitive data in Ansible Vault
- Tags for selective execution
- Idempotent playbooks
- Use `ansible-lint` before committing

### Kubernetes Manifests
- Use declarative configuration
- Organize by namespace and component
- Use kustomize for environment-specific configs
- Implement resource limits
- Use labels consistently

## Documentation

### README Structure
1. Overview
2. Requirements
3. Installation
4. Configuration
5. Usage
6. Examples
7. Troubleshooting
8. Contributing

### Comments
- Explain "why" not "what"
- Keep comments up-to-date
- Remove commented-out code
- Use TODO/FIXME/NOTE appropriately

## Version Control

### Commit Messages
Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat(terraform): add AWS VPC module

Add reusable VPC module with public/private subnets,
NAT gateway, and internet gateway.

Closes #123
```

### Branching Strategy
- `main` - production-ready code
- `develop` - integration branch
- `feature/<name>` - new features
- `fix/<name>` - bug fixes
- `hotfix/<name>` - production hotfixes

## Tools and Editors

### Preferred Tools
- IDE: VSCode
- Terminal: iTerm2/Windows Terminal
- Version Control: Git
- Cloud CLI: aws-cli, azure-cli, gcloud

### VSCode Extensions
- HashiCorp Terraform
- YAML
- Python
- Docker
- Kubernetes
- GitLens
- markdownlint

## Security

### Secrets Management
- Never commit secrets to version control
- Use environment variables or secret managers
- Rotate credentials regularly
- Use `.gitignore` for sensitive files

### Access Control
- Use SSH keys, not passwords
- Implement MFA where possible
- Follow least privilege principle
- Regular access reviews
