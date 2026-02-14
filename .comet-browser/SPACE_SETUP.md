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

### How Agents Identify Themselves

Each Perplexity account derives its agent ID from its profile username:

- atnp1 → comet-atnp1 (red theme)
- atnp2 → comet-atnp2 (yellow theme)  
- atnp3 → comet-atnp3 (blue theme)

In GitHub comments:

```html
<!-- agent:comet-atnp3 -->
@atngit2 [your message here]
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
2. Claim task by commenting "<!-- agent:AGENT_ID --> @atngit2 claiming this task"
3. Add label: claimed → in-progress → review → close
4. Update progress regularly
5. Document all work in issue comments

Timeouts are defined in manifest.json. Check AGENT_PROTOCOL.md for current values.
```

### Default Model & Mode

- **Model:** GPT-5.1 (or your preferred model)
- **Mode:** Research (for thorough investigation)
- **Temperature:** Default

### Files to Attach

Add these files from the atnplex/ai repository as **Space-level files**:

1. `.comet-browser/AGENT_PROTOCOL.md` - Core coordination protocol
2. `.comet-browser/ONBOARDING_CHECKLIST.md` - Setup checklist
3. `.comet-browser/COMET_BOOTSTRAP.md` - Bootstrap instructions

**How to add:**
1. Download or export each file from GitHub
2. In Perplexity Space → Files section (right sidebar)
3. Upload each file
4. These will auto-load as context for ALL threads in this Space

## Quick Start Checklist

- [ ] Read manifest.json to understand protocol version and configuration
- [ ] Derive your agent ID from your Perplexity profile username
- [ ] Check AGENT_PROTOCOL.md for current coordination rules
- [ ] Review atnplex/ai/rules/ for domain guidelines  
- [ ] Find open tasks: https://github.com/atnplex/ai/issues?q=is:open+label:agent-task
- [ ] Claim a task using the proper comment format
- [ ] Update issue with progress regularly
- [ ] Mark as complete when done

## Related Documentation

- [AGENT_PROTOCOL.md](./.AGENT_PROTOCOL.md) - Agent coordination protocol
- [COMET_BOOTSTRAP.md](./COMET_BOOTSTRAP.md) - Bootstrap procedures
- [VERIFICATION_CHECKLIST.md](./VERIFICATION_CHECKLIST.md) - Verification steps
- [manifest.json](../manifest.json) - Protocol configuration
