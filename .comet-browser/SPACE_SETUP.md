# Perplexity Space Setup Guide

**Space Name:** `Perplexity Co-op Hub | atnplex`

**Purpose:** Multi-agent coordination hub for 3 Perplexity Pro accounts collaborating via GitHub SSOT

## Space-Level Configuration

### Space Description

Use this as your Space description:

```
Multi-agent coordination hub for 3 Perplexity Pro accounts working collaboratively via GitHub SSOT (atnplex/ai).

🔗 Primary Repo: github.com/atnplex/ai
👤 GitHub Account: @atngit2 (student dev benefits)
🏢 Organization: @atnplex

⚠️ CRITICAL: Before ANY task, check github.com/atnplex/ai/.comet-browser/ for protocols.

All agents MUST follow AGENT_PROTOCOL.md for task coordination.
```

### Space Instructions

Navigate to Space Settings → Instructions and add:

```
You are an agent in a 3-agent Perplexity Pro coordination system.

BEFORE EVERY TASK:
1. Check atnplex/ai/.comet-browser/AGENT_PROTOCOL.md
2. Review atnplex/ai/rules/ for domain guidelines
3. Check GitHub Issues: is:open label:agent-task
4. Verify no other agent claimed the task

ALWAYS USE:
- GitHub Org: atnplex
- GitHub Account: @atngit2
- Primary Repo: atnplex/ai

WORKFLOW:
1. Find task in GitHub Issues with label:agent-task
2. Claim task by commenting "@agent-[N] claiming this task"
3. Add label: claimed → in-progress → review → close
4. Update progress every 30 minutes
5. Document all work in issue comments

STATE TIMEOUTS:
- claimed: 5 minutes
- in-progress: 2 hours
- review: 24 hours

If timeout exceeded, mark as stale and move to next task.
```

### Default Model & Mode

- **Model:** GPT-5.1 (or your preferred model)
- **Mode:** Research (for thorough investigation)
- **Temperature:** Default

### Files to Attach

Add these files from the atnplex/ai repository as **Space-level files**:

1. `.comet-browser/AGENT_PROTOCOL.md` - Core coordination protocol
2. `.comet-browser/ONBOARDING_CHECKLIST.md` - Setup checklist
3. `.comet-browser/AGENT_PROTOCOL.md` - Task state machine details

**How to add:**
1. Download or export each file from GitHub
2. In Perplexity Space → Files section (right sidebar)
3. Upload each file
4. These will auto-load as context for ALL threads in this Space

### Links to Add

Add these links in the Space → Links section:

- `https://github.com/atnplex/ai`
- `https://github.com/orgs/atnplex/repositories`
- `https://github.com/atnplex/ai/issues?q=is%3Aopen+label%3Aagent-task`
- `https://github.com/atnplex/ai/tree/main/.comet-browser`
- `https://github.com/atnplex/ai/tree/main/rules`

**Why:** This biases the AI toward using these as authoritative sources.

## Per-Thread Optimization

Within individual threads in this Space:

### Task-Specific Setup

1. **Start every thread with:**
   ```
   Task: [Brief description]
   Issue: atnplex/ai#[issue-number]
   Agent: Agent-[N]
   Status: [claimed/in-progress/review]
   ```

2. **Attach task-specific files:**
   - Relevant code files
   - Previous logs or outputs
   - Reference documentation

3. **Override instructions if needed:**
   - "For this task only, focus on X repo"
   - "Use faster model for quick iteration"
   - "Skip verification step (emergency fix)"

### Thread Naming Convention

Use this format for thread titles:
```
[Agent-N] Task #[issue] - [Brief description]
```

Examples:
- `[Agent-1] Task #42 - Setup OCI automation`
- `[Agent-2] Task #43 - Debug GitHub Actions`
- `[Agent-3] Task #44 - Document API changes`

## Scheduled Tasks (Space-Level)

Create these recurring tasks in Space → Scheduled Tasks:

### Daily Status Check
```
Schedule: Every day at 9:00 AM PST
Prompt:
Check atnplex/ai GitHub Issues:
1. List all open issues with label:agent-task
2. Identify any stale tasks (in-progress > 2 hours)
3. Check for tasks in review > 24 hours
4. Summarize status and post to GitHub Discussions
```

### Stale Task Monitor
```
Schedule: Every 2 hours
Prompt:
Scan atnplex/ai issues:
1. Find tasks with label:in-progress
2. Check timestamp on last comment
3. If > 2 hours, add comment: "⚠️ Task may be stale, checking agent status"
4. Wait 30 min, if no response, mark as stale
```

### Weekly Coordination Report
```
Schedule: Every Monday at 8:00 AM PST
Prompt:
Generate weekly report for atnplex/ai:
1. Tasks completed last week
2. Tasks currently in progress
3. Blocked or stale tasks
4. Agent activity summary
5. Post to GitHub Discussions
```

## GitHub Connector Setup

### Enable GitHub Connector

1. Go to Perplexity Settings → Connectors
2. Find "GitHub" and click Connect
3. Authenticate with `@atngit2` credentials
4. Grant permissions to `atnplex` organization
5. Verify connection is active

### Test Connection

Run this query in the Space:
```
List all open issues in atnplex/ai with label:agent-task
```

Should return current task list from GitHub.

### Permissions Needed

- Read/Write Issues
- Read/Write Comments
- Read Repositories
- Read Organization
- (Optional) Write Pull Requests if using PR workflow

## Multi-Agent Coordination

### How Agents Identify Themselves

Each Perplexity Pro account should:

1. **Name your profile:**
   - Account 1: "Agent-1 (Primary)"
   - Account 2: "Agent-2 (Secondary)"  
   - Account 3: "Agent-3 (Tertiary)"

2. **In GitHub comments, always use:**
   - `@agent-1` for Account 1
   - `@agent-2` for Account 2
   - `@agent-3` for Account 3

3. **In thread titles, prefix:**
   - `[Agent-1]` 
   - `[Agent-2]`
   - `[Agent-3]`

### Sharing Space Access

1. **Invite other accounts:**
   - Go to Space Settings
   - Click "Add Contributors"
   - Enter email addresses of other Perplexity accounts
   - Set permissions: "Can edit"

2. **Each agent sees:**
   - Same Space files
   - Same Space instructions
   - Same Space links
   - All threads created in the Space

3. **Threads are NOT automatically shared:**
   - To share a thread, manually "Add to Space"
   - Better: Create threads directly from within the Space

## Troubleshooting

### GitHub Connector Not Working

1. Check authentication: Settings → Connectors → GitHub
2. Re-authenticate if needed
3. Verify `atngit2` has access to `atnplex` org
4. Check GitHub token hasn't expired

### Space Instructions Not Being Followed

- Space instructions are suggestions, not hard rules
- Reinforce in each prompt: "Follow AGENT_PROTOCOL.md"
- Add critical rules as Space files (higher priority)

### Files Not Loading

- Space files have size limits (check current limit)
- Re-upload if file was corrupted
- Verify file is in correct format (markdown, text, etc.)

### Agents Conflicting on Same Task

- Follow AGENT_PROTOCOL.md conflict resolution
- First comment timestamp wins
- Losing agent must unclaim and find new task
- Document in GitHub issue for transparency

## Best Practices

1. **Keep Space clean:**
   - Archive completed threads
   - Remove outdated files
   - Update instructions as protocols evolve

2. **Use consistent naming:**
   - Always prefix with [Agent-N]
   - Reference GitHub issue numbers
   - Use clear, descriptive titles

3. **Document everything:**
   - Every decision in GitHub comments
   - Thread outcomes summarized in issues
   - Update docs when protocols change

4. **Regular maintenance:**
   - Weekly review of Space settings
   - Monthly audit of attached files
   - Quarterly protocol updates

## Quick Start Checklist

- [ ] Rename Space to "Perplexity Co-op Hub | atnplex"
- [ ] Update Space description
- [ ] Add Space instructions
- [ ] Upload AGENT_PROTOCOL.md to Space files
- [ ] Upload ONBOARDING_CHECKLIST.md to Space files
- [ ] Upload AGENT_PROTOCOL.md to Space files
- [ ] Add all GitHub links to Space links
- [ ] Enable GitHub connector with @atngit2
- [ ] Test connector with query
- [ ] Create 3 scheduled tasks (daily, every 2h, weekly)
- [ ] Invite other 2 Perplexity accounts as contributors
- [ ] Create first test task in GitHub Issues
- [ ] Verify all 3 agents can see and claim task

## Maintenance Schedule

- **Daily:** Check scheduled task outputs
- **Weekly:** Review open issues, update stale tasks
- **Monthly:** Audit Space files and settings
- **Quarterly:** Review and update protocols

## Advanced: Browser Control (Comet)

If using Comet browser extension:

1. Each agent has Comet installed in their browser profile
2. Space instructions apply to browser tasks
3. Document browser actions in GitHub comments:
   ```
   @agent-1 executed browser task:
   - Navigated to [URL]
   - Filled form [details]
   - Submitted [result]
   ```

4. For long browser workflows, create sub-tasks in GitHub
5. Share screenshots/logs in issue comments

## Related Documentation

- `AGENT_PROTOCOL.md` - Core coordination protocol
- `AGENT_PROTOCOL.md` - Task state machine details
- `ONBOARDING_CHECKLIST.md` - New agent setup
- `../rules/` - Domain-specific guidelines
