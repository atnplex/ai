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


## 🔄 Task Lifecycle

### State Machine
```
[OPEN] → claim → [CLAIMED] → start → [IN-PROGRESS] → complete → [COMPLETED]
                     ↓                       ↓
                 timeout               [BLOCKED]/[FAILED]
```

### Required Actions
1. **Claiming**: Add `claimed` label, assign yourself, comment with start time
2. **In-Progress**: Remove `claimed`, add `in-progress`, comment with plan
3. **Completing**: Remove `in-progress`, add `completed`, document deliverables
4. **Failing**: Add `failed` label, document reason, unassign

## 📋 Rules and Validation

All agents MUST follow rules in `/rules/` directory:

- **[operational-mcp-management.md](../rules/operational-mcp-management.md)**: MCP server coordination
- **[state-validation.md](../rules/state-validation.md)**: State transition validation

### Pre-Task Validation Checklist
- [ ] Read AGENT_PROTOCOL.md
- [ ] Check domain-specific rules in /rules/
- [ ] Verify issue has `agent-task` label
- [ ] Confirm no `claimed`/`in-progress` labels
- [ ] Check no assignee
- [ ] Review acceptance criteria

## ⚠️ Critical Reminders

### ALWAYS
✅ Read AGENT_PROTOCOL.md before EVERY task
✅ Claim tasks with proper labels and comments
✅ Document all work in issue comments
✅ Update state labels when transitioning
✅ Complete verification checklist before marking done

### NEVER
❌ Claim tasks without commenting
❌ Work on unclaimed tasks
❌ Override another agent's claim
❌ Skip state transitions
❌ Leave tasks in limbo (always resolve)

## 🎯 Best Practices

1. **Communication**: Over-communicate in issue comments
2. **Atomicity**: Keep tasks small and focused
3. **Verification**: Always test deliverables
4. **Documentation**: Update relevant docs
5. **Coordination**: Check for conflicts before starting

## 🛠️ Troubleshooting

### Task Timeout
- Check claim timestamp
- 30min for `claimed`: escalate or release
- 4hr for `in-progress`: mark as `blocked`

### Conflicts
- Refresh issue before claiming
- If race condition: defer to earlier timestamp
- Use issue comments to coordinate

### Blocked Tasks
- Add `blocked` label
- Document blocker in comments
- @mention relevant agents
- Do NOT auto-fail blocked tasks

## 📞 Communication Channels

### Primary: GitHub Issues
- All coordination happens in issues
- Use @mentions for specific agents
- Document decisions in comments

### Secondary: Perplexity Space
- Reference links to protocol docs
- Space instructions point to GitHub
- Discussions happen in threads

## 🏁 Getting Help

If stuck or confused:
1. Re-read [AGENT_PROTOCOL.md](./AGENT_PROTOCOL.md)
2. Check [ONBOARDING_CHECKLIST.md](./ONBOARDING_CHECKLIST.md)
3. Review completed issues for examples
4. Create issue with `agent-urgent` label
5. @mention all agents for coordination

## 📊 Issue Templates

Use GitHub issue templates for consistency:
- **Agent Task**: Structured task template with all required fields
- Located at: `.github/ISSUE_TEMPLATE/`

---

**Last Updated**: 2026-01-20
**Maintained by**: @atngit2
**Questions**: Create issue with label `agent-question`
