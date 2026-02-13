# Agent Coordination Protocol

**Version:** 1.0  
**Last Updated:** 2026-02-13  
**Status:** ACTIVE

## Overview

This protocol defines how 3 Perplexity Pro accounts coordinate through GitHub as Single Source of Truth (SSOT). Each agent operates independently but follows this protocol for task management, communication, and state synchronization.

## Critical Configuration

### Identity
- **GitHub Organization:** `atnplex`
- **GitHub Account:** `@atngit2` (student account with dev benefits)
- **Primary Repository:** `atnplex/ai`
- **Coordination Folder:** `.comet-browser/`

### Agent Naming Convention
- Agent-1 (Primary)
- Agent-2 (Secondary)
- Agent-3 (Tertiary)

## Mandatory First Action: Bootstrap Check

**BEFORE ANY TASK**, every agent MUST:

1. Read `atnplex/ai/.comet-browser/AGENT_PROTOCOL.md` (this file)
2. Check `atnplex/ai/rules/` for domain-specific guidelines
3. Review open GitHub Issues with label `agent-task`
4. Verify no other agent is working on the same task

## Task Lifecycle State Machine

### States

```
backlog → claimed → in-progress → review → completed
                ↓                    ↓
              stale              blocked
```

### State Definitions

| State | Label | Description | Timeout |
|-------|-------|-------------|--------|
| **backlog** | `agent-task` | Task ready to be claimed | N/A |
| **claimed** | `agent-task`, `claimed` | Agent has claimed task | 5 min |
| **in-progress** | `agent-task`, `in-progress` | Agent actively working | 2 hours |
| **blocked** | `agent-task`, `blocked` | Waiting on external dependency | Manual |
| **review** | `agent-task`, `review` | Work complete, needs verification | 24 hours |
| **completed** | Closed issue | Task finished | N/A |
| **stale** | `agent-task`, `stale` | Timeout exceeded | Auto-detected |

## Task Claiming Protocol

### How to Claim a Task

1. **Find unclaimed task:**
   - Filter: `is:open label:agent-task -label:claimed -label:in-progress`

2. **Claim the task:**
   - Add comment: `@agent-[N] claiming this task`
   - Add label: `claimed`
   - Add assignee: yourself (if possible)
   - Record timestamp in comment

3. **Start work within 5 minutes:**
   - Update label from `claimed` → `in-progress`
   - Add comment: `@agent-[N] starting work`

### If Task is Already Claimed

- Check timestamp on claim comment
- If `claimed` > 5 min → Comment asking for status, wait 10 min, then reclaim if no response
- If `in-progress` > 2 hours → Comment asking for status, wait 30 min, then mark as `stale`

## Work Progress Updates

While `in-progress`, update every 30 minutes:

```markdown
@agent-[N] progress update:
- [x] Completed subtask 1
- [ ] Working on subtask 2
- [ ] Pending subtask 3

ETA: [time estimate]
```

## Task Completion Protocol

1. **Mark task for review:**
   - Update label: `in-progress` → `review`
   - Add comment with summary:
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

2. **Wait for verification:**
   - Another agent should verify within 24 hours
   - If verified, close issue with comment: `@agent-[N] verified and closing`
   - If issues found, reopen with `in-progress` label

## Conflict Resolution

### Multiple Agents Claim Same Task
- First comment timestamp wins
- Other agents must unclaim and find different task

### Task Becomes Blocked
- Add label: `blocked`
- Remove: `in-progress`
- Add comment explaining blocker:
  ```markdown
  @agent-[N] blocked by:
  - Reason for block
  - What's needed to unblock
  ```
- Find another task

### Stale Task Detection
- Any agent can mark tasks as `stale` if timeout exceeded
- Add comment: `@agent-[N] marking as stale due to timeout`
- Remove `in-progress`, add `stale`
- Task returns to `backlog` (remove all state labels except `agent-task`)

## Communication Protocol

### Where to Communicate
- **Task-specific:** In GitHub Issue comments
- **General coordination:** `atnplex/ai` Discussions
- **Urgent/blocking:** Create new issue with label `agent-urgent`

### Comment Format
```markdown
@agent-[N] [ACTION] [context]

Optional details...
```

Examples:
- `@agent-2 claiming this task`
- `@agent-1 question: how should I handle edge case X?`
- `@agent-3 blocked by: need API credentials`

## File Change Protocol

### For Code/Config Changes
1. Create branch: `agent-[N]/[task-id]-[description]`
2. Make changes
3. Commit with message: `[#issue-number] Description`
4. Push and create PR
5. Link PR to issue
6. Update issue to `review` state

### For Documentation
- Can commit directly to `main` for minor docs
- Use PR for major documentation changes

## Automation Rules

### Auto-Stale Detection (Future)
- Bot checks every 30 minutes
- Marks tasks as `stale` if timeout exceeded
- Posts warning comment at 50% of timeout

### Auto-Assignment (Future)
- Bot can suggest tasks to idle agents
- Based on agent expertise/history

## Best Practices

1. **Always check SSOT first** - Never assume task state
2. **Communicate clearly** - Use @mentions and status labels
3. **Update frequently** - Don't go silent for > 30 min on active tasks
4. **Verify before closing** - Another agent should verify work
5. **Document decisions** - Add comments explaining "why" not just "what"
6. **Handle failures gracefully** - If you can't complete, document and unclaim
7. **Be specific in commits** - Reference issue numbers and describe changes
8. **Test before marking review** - Verify your work locally/manually first

## Emergency Procedures

### System is Down
- If GitHub is down, pause all work
- Do not make changes without ability to log them
- Wait for GitHub to recover

### Agent Credentials Compromised
- Immediately revoke access
- Create issue with label `agent-urgent` and `security`
- Rotate credentials

### Conflicting Changes
- GitHub will show merge conflicts
- Agent who pushed last must resolve
- If unclear, discuss in issue comments

## Quick Reference

### GitHub Issue Filters

```
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
```

### State Transition Checklist

- [ ] `backlog` → `claimed`: Add claim comment, add label
- [ ] `claimed` → `in-progress`: Add start comment, update label (< 5 min)
- [ ] `in-progress` → `review`: Add completion comment, update label
- [ ] `review` → `completed`: Add verification comment, close issue
- [ ] Any → `blocked`: Add block comment, add label
- [ ] Any → `stale`: Add stale comment, reset to backlog

## Changelog

- **2026-02-13**: Initial protocol v1.0 created
