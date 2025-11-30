# Chain of Thought Template: Security Review

Use this template when conducting security reviews or assessments.

## Step 1: Scope Definition
**Think through:**
- What system/component is being reviewed?
- What are the boundaries?
- What assets need protection?
- What are the threat models?

**Document:**
```
Scope: [System/component]
Boundaries: [What's included/excluded]

Assets:
- [Asset 1]: [Classification]
- [Asset 2]: [Classification]

Threat Actors:
- [Type 1]: [Capability level]
```

## Step 2: Authentication and Authorization
**Think through:**
- How are users authenticated?
- Is MFA implemented?
- How is authorization enforced?
- Are privileges least-privilege?
- How are service accounts managed?

**Document:**
```
Authentication:
- Method: [Description]
- MFA: [Yes/No - Details]
- Issues: [List any concerns]

Authorization:
- Model: [RBAC/ABAC/etc]
- Implementation: [Description]
- Privilege Level: [Assessment]
- Issues: [List any concerns]
```

## Step 3: Data Protection
**Think through:**
- Is data encrypted at rest?
- Is data encrypted in transit?
- How are secrets managed?
- Are backups encrypted?
- What is the key management strategy?

**Document:**
```
Encryption at Rest:
- Status: [Yes/No]
- Method: [Algorithm/service]
- Issues: [List any concerns]

Encryption in Transit:
- Status: [Yes/No]
- Protocol: [TLS version]
- Issues: [List any concerns]

Secrets Management:
- Method: [Service/tool]
- Rotation: [Policy]
- Issues: [List any concerns]
```

## Step 4: Network Security
**Think through:**
- Is network segmentation implemented?
- Are security groups properly configured?
- Are there any exposed services?
- Is there a DMZ architecture?
- Are there network access controls?

**Document:**
```
Network Segmentation: [Yes/No - Details]
Exposed Services: [List]
Firewall Rules: [Assessment]
Access Controls: [Assessment]
Issues: [List any concerns]
```

## Step 5: Logging and Monitoring
**Think through:**
- What security events are logged?
- How long are logs retained?
- Are logs monitored for threats?
- Are there alerts for suspicious activity?
- Is there an incident response plan?

**Document:**
```
Logging:
- Events Logged: [List]
- Retention: [Duration]
- Protection: [Integrity measures]

Monitoring:
- SIEM: [Yes/No - Tool]
- Alerts: [List key alerts]
- Response Plan: [Yes/No]

Issues: [List any concerns]
```

## Step 6: Compliance and Policies
**Think through:**
- What compliance requirements apply?
- Are security policies documented?
- Are there regular audits?
- Is there security training?

**Document:**
```
Compliance: [Frameworks/standards]
Policies: [List key policies]
Audits: [Frequency]
Training: [Program details]
Issues: [List any gaps]
```

## Step 7: Vulnerability Assessment
**Think through:**
- Are there known vulnerabilities?
- When was the last security scan?
- Are dependencies up to date?
- Are there any misconfigurations?

**Document:**
```
Vulnerabilities:
- [CVE/Issue 1]: [Severity] - [Status]

Last Scan: [Date]
Scan Tools: [List]
Patch Status: [Assessment]
Issues: [List findings]
```

## Step 8: Recommendations
**Think through:**
- What are the critical findings?
- What are quick wins?
- What requires long-term planning?
- What is the priority order?

**Document:**
```
Critical (Fix Immediately):
- [Finding 1]: [Recommendation]

High Priority (Fix within 30 days):
- [Finding 2]: [Recommendation]

Medium Priority (Fix within 90 days):
- [Finding 3]: [Recommendation]

Long-term Improvements:
- [Recommendation 1]
```
