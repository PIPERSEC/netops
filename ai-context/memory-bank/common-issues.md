# Common Issues and Solutions

## Infrastructure

### Issue: Terraform State Lock
**Problem**: State file is locked and preventing operations
**Solution**:
```bash
# Force unlock (use with caution)
terraform force-unlock <lock-id>

# Verify state
terraform state list
```

### Issue: AWS Authentication Failures
**Problem**: Cannot authenticate to AWS
**Solution**:
1. Verify credentials: `aws sts get-caller-identity`
2. Check environment variables: `AWS_PROFILE`, `AWS_REGION`
3. Verify IAM permissions
4. Check credential expiration

## Kubernetes

### Issue: Pods in CrashLoopBackOff
**Problem**: Pod keeps restarting
**Solution**:
```bash
# Check logs
kubectl logs <pod-name> --previous

# Describe pod for events
kubectl describe pod <pod-name>

# Common causes:
# - Missing dependencies
# - Incorrect health check configuration
# - Insufficient resources
# - Application errors
```

### Issue: ImagePullBackOff
**Problem**: Cannot pull container image
**Solution**:
1. Verify image exists and tag is correct
2. Check image pull secrets
3. Verify network connectivity to registry
4. Check registry authentication

## Ansible

### Issue: SSH Connection Failures
**Problem**: Cannot connect to managed hosts
**Solution**:
1. Verify SSH key permissions (600)
2. Check inventory file
3. Verify SSH port and connectivity
4. Check `ansible_user` variable
5. Use `-vvv` for verbose debugging

## Docker

### Issue: Permission Denied
**Problem**: Docker commands fail with permission errors
**Solution**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or:
newgrp docker
```

## General Debugging

### Systematic Approach
1. Check logs first
2. Verify configuration
3. Check permissions
4. Verify network connectivity
5. Check resource availability
6. Review recent changes
7. Consult documentation

### Useful Commands
```bash
# System resources
top, htop, free -h, df -h

# Network
netstat -tulpn, ss -tulpn, ping, traceroute, nslookup

# Logs
journalctl -u <service>, tail -f /var/log/<logfile>

# Processes
ps aux | grep <process>, pgrep, pkill
```
