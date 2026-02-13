# Perplexity Multi-Agent Coordination System

**Organization:** atnplex  
**Primary Repository:** atnplex/ai  
**GitHub Account:** @atngit2 (student dev benefits)  
**Perplexity Space:** [Perplexity Co-op Hub | atnplex](https://www.perplexity.ai/spaces/perplexity-co-op-hub-atnplex-VnIa20avQIWrzaEDL4T2eQ)

## 🎯 Purpose

This folder contains the coordination protocols and documentation for a 3-agent Perplexity Pro system using GitHub as Single Source of Truth (SSOT). Agents work independently but coordinate through GitHub Issues, following strict protocols to avoid conflicts and ensure efficient collaboration.

## 📚 Documentation

### Core Documents (READ IN ORDER)

1. **[AGENT_PROTOCOL.md](./AGENT_PROTOCOL.md)** ⭐ **START HERE**
   - Complete coordination protocol
   - Task lifecycle state machine
   - Claiming, execution, and completion workflows
   - Timeout rules and conflict resolution
   - **Must read BEFORE every task**

2. **[SPACE_SETUP.md](./SPACE_SETUP.md)**
   - Perplexity Space configuration guide
   - GitHub connector setup
   - Scheduled tasks templates
   - Troubleshooting and maintenance

3. **[ONBOARDING_CHECKLIST.md](./ONBOARDING_CHECKLIST.md)**
   - New agent setup guide
   - 7-phase onboarding process
   - Verification and certification
   - Quick reference section

## 🚀 Quick Start

### For New Agents

1. **Read documentation in order** (see above)
2. **Complete onboarding checklist** 
3. **Join Perplexity Space**: [Perplexity Co-op Hub](https://www.perplexity.ai/spaces/perplexity-co-op-hub-atnplex-VnIa20avQIWrzaEDL4T2eQ)
4. **Connect GitHub**: Settings → Connectors → GitHub (use @atngit2)
5. **Practice with test task** before taking real tasks

### For Active Agents

**BEFORE EVERY TASK:**
```bash
# 1. Check protocol
Read: github.com/atnplex/ai/.comet-browser/AGENT_PROTOCOL.md

# 2. Check domain guidelines  
Read: github.com/atnplex/ai/rules/

# 3. Find available tasks
GitHub Issues: is:open label:agent-task -label:claimed -label:in-progress

# 4. Verify no conflicts
Check no other agent claimed the task
```

## 🏷️ GitHub Labels

Create these labels in the atnplex/ai repository:

| Label | Color | Description | Timeout |
|-------|-------|-------------|--------|
| `agent-task` | Purple | Task available for agents | N/A |
| `claimed` | Yellow | Agent has claimed task | 5 min |
| `in-progress` | Blue | Agent actively working | 2 hours |
| `review` | Green | Work complete, needs verification | 24 hours |
| `blocked` | Red | Waiting on external dependency | Manual |
| `stale` | Gray | Timeout exceeded | Auto |
| `agent-urgent` | Orange | Urgent/blocking issue | Immediate |

## 🔄 Task Workflow

```
┌─────────┐    claim      ┌─────────┐    start      ┌────────────┐
│ backlog │──────────────▶│ claimed │──────────────▶│in-progress │
└─────────┘    +comment    └─────────┘    <5 min     └────────────┘
                                                            │
                                                         complete
                                                            │
                                                            ▼
                                                      ┌─────────┐    verify    ┌───────────┐
                                                      │ review  │────────────▶│ completed │
                                                      └─────────┘    <24 hr    └───────────┘
                                                            │
                                                         blocked
                                                            ▼
                                                      ┌─────────┐
                                                      │ blocked │
                                                      └─────────┘
```

**Timeouts:**
- `claimed` → `stale`: 5 minutes
- `in-progress` → `stale`: 2 hours  
- `review` → `stale`: 24 hours

## 👥 Agent IDs

- **Agent-1** (Primary) - First account
- **Agent-2** (Secondary) - Second account
- **Agent-3** (Tertiary) - Third account

**Use in comments:** `@agent-[N] [action] [context]`

Example: `@agent-2 claiming this task`

## 📋 Essential Commands

### Find Tasks
```bash
# Available tasks
is:open label:agent-task -label:claimed -label:in-progress

# My active tasks
is:open label:agent-task assignee:@me

# Stale tasks needing attention
is:open label:agent-task label:stale

# Blocked tasks
is:open label:agent-task label:blocked

# Tasks in review
is:open label:agent-task label:review

# Urgent issues
is:open label:agent-urgent
```

### Claim a Task
1. Add comment: `@agent-[N] claiming this task`
2. Add label: `claimed`
3. (Optional) Assign to yourself
4. Within 5 min: Update to `in-progress`

### Update Progress
```markdown
@agent-[N] progress update:
- [x] Completed subtask 1
- [ ] Working on subtask 2
- [ ] Pending subtask 3

ETA: 30 minutes
```

### Mark for Review
```markdown
@agent-[N] task complete

**Work done:**
- Item 1
- Item 2

**Files changed:**
- path/to/file1
- path/to/file2

**Verification steps:**
1. Check X
2. Verify Y
```

## 🔗 Important Links

### GitHub
- **Main Repo**: https://github.com/atnplex/ai
- **Organization**: https://github.com/orgs/atnplex/repositories
- **Issues Board**: https://github.com/atnplex/ai/issues
- **Agent Tasks**: https://github.com/atnplex/ai/issues?q=is%3Aopen+label%3Aagent-task
- **Coordination Folder**: https://github.com/atnplex/ai/tree/main/.comet-browser
- **Rules**: https://github.com/atnplex/ai/tree/main/rules

### Perplexity
- **Shared Space**: https://www.perplexity.ai/spaces/perplexity-co-op-hub-atnplex-VnIa20avQIWrzaEDL4T2eQ

## ⚙️ Configuration

### GitHub Settings
- **Organization**: atnplex
- **Account**: @atngit2
- **Permissions**: Read/Write Issues, Comments, Repositories

### Perplexity Space Settings
- **Space Instructions**: Configured with agent protocol
- **Files**: AGENT_PROTOCOL.md, SPACE_SETUP.md, ONBOARDING_CHECKLIST.md (to be added)
- **Links**: GitHub repos configured
- **Model**: GPT-5.1 (or preferred)
- **Mode**: Research (default)

## 🛠️ Maintenance

### Daily
- Check for `agent-urgent` issues
- Review your `in-progress` tasks
- Verify other agents' completed work
- Mark stale tasks if timeouts exceeded

### Weekly
- Review open issues and clean up
- Update documentation if protocols changed
- Check scheduled task outputs

### Monthly
- Audit Space settings
- Review and update protocol documentation
- Check GitHub connector health

## 🚨 Emergency Procedures

### Multiple Agents Claim Same Task
1. Check timestamps on claim comments
2. Earlier timestamp wins
3. Later agent must unclaim immediately

### Task Becomes Stale
1. Any agent can mark as `stale` if timeout exceeded
2. Add comment: `@agent-[N] marking as stale due to timeout`
3. Remove all state labels except `agent-task`
4. Task returns to backlog

### System Down
- If GitHub is down, pause all work
- Do not make changes without ability to log them
- Wait for GitHub to recover

### Agent Credentials Compromised
1. Immediately revoke access
2. Create issue with `agent-urgent` + `security` labels
3. Rotate credentials

## 📊 Metrics & Monitoring

### Key Metrics to Track
- Tasks completed per week
- Average time in each state
- Stale task frequency
- Agent response time to @mentions
- Conflict rate (multiple claims)

### Monitoring (Future)
- Automated stale task detection
- Daily status reports via scheduled tasks
- Weekly coordination summaries
- Agent activity dashboards

## 🔐 Security & Privacy

- Never commit sensitive credentials to GitHub
- Use GitHub Secrets for API keys
- Keep coordination in public repos (except sensitive data)
- Log all actions in GitHub Issues for transparency
- Each agent operates with same permissions

## 🤝 Contributing

### Updating Protocols
1. Create issue with `agent-urgent` label
2. Discuss changes with all agents
3. Update documentation via PR
4. Notify all agents of changes
5. Update Space instructions if needed

### Reporting Issues
1. Create GitHub Issue
2. Add appropriate labels
3. @mention relevant agents
4. For urgent: use `agent-urgent` label

## 📖 Additional Resources

### GitHub
- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [GitHub Labels Guide](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work)
- [GitHub Markdown Syntax](https://docs.github.com/en/get-started/writing-on-github)

### Perplexity
- [Perplexity Spaces Guide](https://www.perplexity.ai/help-center/en/articles/10352961-what-are-spaces)
- [GitHub Connector](https://www.perplexity.ai/help-center/en/articles/12275669-github-connector-for-enterprise)

## 📝 Version History

- **v1.0** (2026-02-13): Initial coordination system setup
  - Created AGENT_PROTOCOL.md
  - Created SPACE_SETUP.md
  - Created ONBOARDING_CHECKLIST.md
  - Configured Perplexity Space
  - Set up GitHub structure

## 💬 Questions?

Create an issue with label `agent-urgent` and @mention all agents:
`@agent-1 @agent-2 @agent-3`

---

**Remember:** Before ANY task, always check [AGENT_PROTOCOL.md](./AGENT_PROTOCOL.md) 🎯
