# Architectural Decision Records (ADRs)

## ADR Template
```
## ADR-XXX: [Title]
Date: YYYY-MM-DD
Status: [Proposed | Accepted | Deprecated | Superseded]

### Context
[Describe the context and problem statement]

### Decision
[Describe the decision and chosen approach]

### Consequences
[Describe the resulting context after applying the decision]

### Alternatives Considered
[List alternative options that were evaluated]
```

## Decisions

### ADR-001: Framework Structure
Date: 2025-11-30
Status: Accepted

#### Context
Need to organize systems engineering work with proper separation of concerns, reusable components, and AI context management.

#### Decision
Implement a directory structure with:
- `/projects` - Active project work
- `/templates` - Reusable templates
- `/docs` - Documentation and runbooks
- `/config` - Tool configurations
- `/ai-context` - AI personas, memory bank, CoT templates
- `/scripts` - Utility scripts
- `/tools` - Custom tooling

#### Consequences
- Clear separation of concerns
- Easy to find and reuse components
- Consistent structure across projects
- Better AI context retention

#### Alternatives Considered
- Monolithic structure
- Project-first organization
- Tool-based organization
