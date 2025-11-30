# Chain of Thought Template: Troubleshooting

Use this template when debugging issues or incidents.

## Step 1: Problem Definition
**Think through:**
- What is the observed behavior?
- What is the expected behavior?
- When did this start?
- What changed recently?
- What is the impact?

**Document:**
```
Issue: [Clear description]
Expected: [What should happen]
Observed: [What is happening]
Started: [When]
Impact: [Severity and scope]
Recent Changes: [List]
```

## Step 2: Data Gathering
**Think through:**
- What logs are relevant?
- What metrics show anomalies?
- What is the system state?
- Are there any error messages?

**Document:**
```
Logs Checked:
- [Log source 1]: [Key findings]
- [Log source 2]: [Key findings]

Metrics:
- [Metric 1]: [Current vs baseline]

Error Messages:
- [Error 1]
```

## Step 3: Hypothesis Formation
**Think through:**
- What could cause this behavior?
- What are the most likely root causes?
- What can be ruled out?

**Document:**
```
Potential Causes:
1. [Hypothesis 1] - Likelihood: High/Medium/Low
   Evidence: [Supporting data]

2. [Hypothesis 2] - Likelihood: High/Medium/Low
   Evidence: [Supporting data]

Ruled Out:
- [Cause]: [Why ruled out]
```

## Step 4: Testing and Validation
**Think through:**
- How can each hypothesis be tested?
- What tests are safe to run in production?
- What is the testing order (most likely first)?

**Document:**
```
Test 1: [Description]
Expected Result: [What this would prove]
Actual Result: [Outcome]

Test 2: [Description]
Expected Result: [What this would prove]
Actual Result: [Outcome]
```

## Step 5: Root Cause Identification
**Think through:**
- Which hypothesis was confirmed?
- What is the underlying cause?
- Why did this happen?
- Why wasn't this caught earlier?

**Document:**
```
Root Cause: [Clear statement]

Contributing Factors:
- [Factor 1]
- [Factor 2]

Why Not Detected:
- [Reason]
```

## Step 6: Resolution
**Think through:**
- What is the immediate fix?
- What is the long-term solution?
- Are there side effects to consider?
- How will we verify the fix?

**Document:**
```
Immediate Fix: [Action taken]
Long-term Solution: [Preventive measures]

Verification:
- [Check 1]
- [Check 2]

Follow-up Actions:
- [Action 1]
```

## Step 7: Post-Mortem
**Think through:**
- What can we learn?
- What processes need improvement?
- How can we prevent recurrence?

**Document:**
```
Lessons Learned:
- [Lesson 1]

Process Improvements:
- [Improvement 1]

Prevention:
- [Preventive measure 1]
```
