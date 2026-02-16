---
name: Skills Standards
description: Defines skill folder structure and SKILL.md format
trigger: always
---

# R92: Skills Standards

> Standardizes skill definitions and discovery.

## Location

| Type             | Location                                              |
| ---------------- | ----------------------------------------------------- |
| Global Skills    | `$NAMESPACE/.gemini/antigravity/skills/<skill-name>/` |
| Workspace Skills | `.agent/skills/<skill-name>/`                         |

## Required Files

Every skill folder MUST contain:

```
<skill-name>/
├── SKILL.md        # Required - Main instruction file
├── scripts/        # Optional - Helper scripts
├── examples/       # Optional - Reference implementations
└── resources/      # Optional - Additional assets
```

## SKILL.md Format

```yaml
---
name: Skill Name
description: Brief description for discovery
triggers:
  - keyword1
  - keyword2
---
# Skill Name

Detailed instructions for the agent...
```

## Discovery

Skills are loaded when:

1. User request contains trigger keywords
2. User explicitly mentions `@skill-name`
3. Domain detection matches skill category

## Current Skills

| Skill                            | Purpose                             | Category       |
| -------------------------------- | ----------------------------------- | -------------- |
| `brainstorming`                  | REQUIRED before creative work       | Required       |
| `verification-before-completion` | REQUIRED before claiming done       | Required       |
| `deploy`                         | Deploy/restart Docker services      | Infrastructure |
| `inventory`                      | Collect system inventory            | Infrastructure |
| `health`                         | Check service health endpoints      | Infrastructure |
| `ssh`                            | SSH connection shortcuts            | Infrastructure |
| `cloudflare-tunnel`              | Manage Cloudflare Tunnels           | Infrastructure |
| `logs`                           | View Docker container logs          | Infrastructure |
| `parallel-research`              | Fast parallel summarization         | AI/Agent       |
| `parallel-agents`                | Dispatch concurrent subagents       | AI/Agent       |
| `ai-reviewer-workflow`           | Optimized AI code review            | AI/Agent       |
| `repomix-optimize`               | Pack repos for LLM consumption      | AI/Agent       |
| `context-compression`            | Reduce token usage                  | Context Mgmt   |
| `context-optimization`           | Maximize context effectiveness      | Context Mgmt   |
| `filesystem-context`             | Filesystem-based context offloading | Context Mgmt   |
| `memory-persistence`             | STM/LTM across sessions             | Context Mgmt   |
| `git-ops`                        | Git add, commit, push               | Development    |
| `environment-check`              | Verify env before commands          | Development    |
| `error-recovery`                 | Graceful failure handling           | Development    |
| `self-reflection`                | Learn from past actions             | Meta           |
| `prompt-optimization`            | Enhance prompts with context        | Meta           |

## Usage Example

When implementing a new feature:

1. Load `brainstorming` skill first
2. Execute skill instructions
3. Proceed with implementation
4. Load `verification-before-completion` before claiming done
