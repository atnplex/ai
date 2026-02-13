# Agent Onboarding Checklist

**Purpose:** Ensure all 3 Perplexity Pro agents are properly configured for multi-agent coordination.

## Prerequisites

- [ ] You have a Perplexity Pro account
- [ ] You have access to GitHub account `@atngit2`
- [ ] You have access to GitHub organization `atnplex`
- [ ] You have Comet browser extension installed (optional but recommended)

## Phase 1: Account Setup

### Perplexity Account Configuration

- [ ] **Set profile name:**
  - Account 1: "Agent-1 (Primary)"
  - Account 2: "Agent-2 (Secondary)"
  - Account 3: "Agent-3 (Tertiary)"

- [ ] **Enable GitHub Connector:**
  1. Go to Settings → Connectors
  2. Find "GitHub" and click Connect
  3. Authenticate with `@atngit2` credentials
  4. Grant permissions to `atnplex` organization
  5. Verify connection successful

- [ ] **Test GitHub Connector:**
  - Run query: `List all repositories in atnplex organization`
  - Verify you see repos including `atnplex/ai`

### GitHub Access Verification

- [ ] **Verify you can access:**
  - https://github.com/atnplex/ai
  - https://github.com/orgs/atnplex/repositories
  - https://github.com/atnplex/ai/issues

- [ ] **Check permissions:**
  - You can create issues
  - You can comment on issues
  - You can add labels
  - You can push to branches (if applicable)

## Phase 2: Space Setup

### Join Shared Space

- [ ] **Accept Space invitation:**
  - Check email for invite to "Perplexity Co-op Hub | atnplex"
  - Accept invitation
  - Verify you can see the Space in your Spaces list

- [ ] **Verify Space settings:**
  - Check Space description mentions `atnplex/ai`
  - Review Space instructions
  - Confirm Space files are visible (Files sidebar)
  - Check Space links include GitHub repos

### Download Critical Documentation

- [ ] **Read these files from `atnplex/ai/.comet-browser/`:**
  - [ ] `AGENT_PROTOCOL.md` - **READ THIS FIRST**
  - [ ] `SPACE_SETUP.md` - Space configuration details
  - [ ] This file (`ONBOARDING_CHECKLIST.md`)

- [ ] **Understand key concepts:**
  - Task lifecycle states (backlog → claimed → in-progress → review → completed)
  - State timeouts (claimed: 5min, in-progress: 2hr, review: 24hr)
  - Conflict resolution (first timestamp wins)
  - Communication protocol (@agent-N format)

## Phase 3: Protocol Training

### Task Claiming Workflow

- [ ] **Learn GitHub Issue filters:**
  ```
  # Available tasks
  is:open label:agent-task -label:claimed -label:in-progress
  
  # My active tasks  
  is:open label:agent-task assignee:@me
  
  # Stale tasks
  is:open label:agent-task label:stale
  ```

- [ ] **Practice task workflow (on test task):**
  1. Find unclaimed task with `label:agent-task`
  2. Add comment: `@agent-[N] claiming this task`
  3. Add label: `claimed`
  4. Within 5 min, change label to `in-progress`
  5. Add progress comment: `@agent-[N] starting work`
  6. Work on task, update every 30 min
  7. Complete and mark as `review`
  8. Wait for another agent to verify

### Communication Protocol

- [ ] **Understand comment format:**
  ```markdown
  @agent-[N] [ACTION] [context]
  
  Optional details...
  ```

- [ ] **Know when to use each channel:**
  - **GitHub Issue comments:** Task-specific discussion
  - **GitHub Discussions:** General coordination
  - **New issue with `agent-urgent`:** Blocking problems

### Conflict Resolution

- [ ] **Know what to do if:**
  - Another agent claims same task → Check timestamps, later claim must unclaim
  - Task times out → Mark as `stale`, remove state labels
  - You get blocked → Add `blocked` label, explain in comment, find new task
  - You need help → Comment in issue or create `agent-urgent` issue

## Phase 4: Verification

### Create Test Task

- [ ] **Agent-1 only:** Create test issue
  ```markdown
  Title: [TEST] Agent coordination practice
  
  Body:
  This is a test task for agent onboarding.
  
  **Task:** Each agent should:
  1. Claim this task
  2. Add a comment with their agent number
  3. Unclaim (remove labels)
  4. Next agent goes
  
  Labels: agent-task
  ```

### Practice Coordination

- [ ] **All agents:** Complete test task workflow
  - [ ] Agent-1: Claim, comment, unclaim
  - [ ] Agent-2: Claim, comment, unclaim
  - [ ] Agent-3: Claim, comment, close issue

- [ ] **Verify you can:**
  - See other agents' comments
  - Add labels to issues
  - Follow the protocol correctly
  - Use proper `@agent-N` format

## Phase 5: Browser Control (Optional)

### Comet Extension Setup

- [ ] **Install Comet:**
  - Install Comet browser extension
  - Create separate browser profile for your agent
  - Sign into Perplexity in that profile

- [ ] **Test browser control:**
  - Ask: "Navigate to github.com/atnplex/ai"
  - Verify browser control works
  - Test basic interactions (click, scroll, read page)

- [ ] **Understand browser task protocol:**
  - Document browser actions in GitHub comments
  - Include screenshots for significant steps
  - Log results and outcomes

## Phase 6: First Real Task

### Find Your First Task

- [ ] **Check for available tasks:**
  - Go to https://github.com/atnplex/ai/issues
  - Filter: `is:open label:agent-task -label:claimed -label:in-progress`
  - Review available tasks

- [ ] **Choose appropriate task:**
  - Start with `good-first-issue` if available
  - Read task description carefully
  - Check if you have skills/access needed
  - Estimate if you can complete within 2 hours

### Execute First Task

- [ ] **Follow protocol exactly:**
  1. Claim task with proper comment
  2. Add `claimed` label
  3. Within 5 min, start work and update to `in-progress`
  4. Update progress every 30 min
  5. Complete work, test/verify
  6. Mark as `review` with completion summary
  7. Wait for verification from another agent

- [ ] **Document everything:**
  - All decisions in comments
  - Any blockers encountered
  - How you resolved issues
  - Final outcome

## Phase 7: Ongoing Operations

### Daily Routine

- [ ] **Morning:**
  - Check for `agent-urgent` issues
  - Review your `in-progress` tasks
  - Check if any tasks assigned to you
  - Review overnight activity from other agents

- [ ] **During work:**
  - Update progress every 30 min on active tasks
  - Respond to @mentions quickly
  - Help verify other agents' completed work
  - Mark stale tasks if you notice timeouts

- [ ] **End of day:**
  - Update status on any in-progress tasks
  - If you can't finish, mark as `blocked` with explanation
  - Don't leave tasks in `claimed` overnight

### Weekly Maintenance

- [ ] **Monday morning:**
  - Review weekly coordination report (from scheduled task)
  - Check for any stale/blocked tasks
  - Plan your work for the week

- [ ] **Friday afternoon:**
  - Complete or hand off in-progress tasks
  - Update documentation if protocols changed
  - Review Space settings for any needed updates

## Troubleshooting

### GitHub Connector Issues

**Problem:** Can't see atnplex repos  
**Solution:**
1. Settings → Connectors → GitHub
2. Disconnect and reconnect
3. Ensure using `@atngit2` credentials
4. Check GitHub hasn't revoked token

**Problem:** Can't comment on issues  
**Solution:**
1. Verify `@atngit2` has write access to `atnplex/ai`
2. Check GitHub token permissions
3. Try commenting directly on GitHub web

### Space Access Issues

**Problem:** Can't see Space files  
**Solution:**
1. Verify you're in the correct Space
2. Check right sidebar for Files section
3. Try refreshing the page
4. Contact Space owner to re-upload files

**Problem:** Space instructions not loading  
**Solution:**
1. Check Space Settings → Instructions
2. Instructions might be empty (manual setup needed)
3. See SPACE_SETUP.md for what should be there

### Coordination Issues

**Problem:** Multiple agents claimed same task  
**Solution:**
1. Check timestamps on claim comments
2. Earlier timestamp wins
3. Later claimant must unclaim immediately
4. Document in comment for transparency

**Problem:** Agent not responding for > 2 hours  
**Solution:**
1. Add comment: `@agent-[N] checking status, task may be stale`
2. Wait 30 minutes
3. If no response, mark task as `stale`
4. Remove state labels, task returns to backlog

## Certification

Once you've completed all phases above:

- [ ] **Post completion comment in test issue:**
  ```markdown
  @agent-[N] completed onboarding checklist
  
  - All phases complete
  - Understand protocol
  - Ready for real tasks
  ```

- [ ] **You are now a certified agent!** Welcome to the team.

## Quick Reference

### Essential Links
- Protocol: https://github.com/atnplex/ai/.comet-browser/AGENT_PROTOCOL.md
- Space Setup: https://github.com/atnplex/ai/.comet-browser/SPACE_SETUP.md
- Issues: https://github.com/atnplex/ai/issues?q=is%3Aopen+label%3Aagent-task
- Organization: https://github.com/orgs/atnplex/repositories

### Key Commands
```bash
# Find available tasks
is:open label:agent-task -label:claimed -label:in-progress

# Find my tasks
is:open label:agent-task assignee:@me

# Find stale tasks
is:open label:agent-task label:stale

# Find urgent tasks
is:open label:agent-urgent
```

### State Timeouts
- **claimed:** 5 minutes
- **in-progress:** 2 hours  
- **review:** 24 hours

### Agent IDs
- Agent-1 (Primary)
- Agent-2 (Secondary)
- Agent-3 (Tertiary)

---

**Questions?** Create an issue with label `agent-urgent` and mention all agents.
