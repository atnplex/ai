# Agent Self-Verification Checklist

**Purpose:** Verify you understand the protocol before claiming tasks

---

## Protocol Knowledge Check

After reading AGENT_PROTOCOL.md, answer these questions:

**Q0: What is the current protocol version?**

<details>
<summary>Answer</summary>

Check manifest.json `protocol_version` field (currently 1.0.0)
</details>

**Q0b: What is your derived agent ID?**

<details>
<summary>Answer</summary>

Formula: comet-{profile_username}
Example: atnp3 → comet-atnp3
</details>

**Q0c: Where are timeout values defined?**
<details>
<summary>Answer</summary>

In manifest.json under `state_timeouts` for each profile
</details>

**Q0d: What is the required comment format for claiming tasks?**

<details>
<summary>Answer</summary>

```html
<!-- agent:AGENT_ID --> @atngit2 [message]
```
Example: `<!-- agent:comet-atnp3 --> @atngit2 claiming this task`
</details>

**Q0e: Which file contains the agent registry?**

<details>
<summary>Answer</summary>

manifest.json in the `registered_profiles` field
</details>

### 1. State Transition Timeouts

**Q: What are the timeout periods for each state?**
- claimed: _____ minutes
- in-progress: _____ hours  
- review: _____ hours

<details>
<summary>Answer</summary>

- claimed: 5 minutes
- in-progress: 2 hours
- review: 24 hours
</details>

### 2. Task Claiming Process

**Q: What's the first action when claiming a task?**

<details>
<summary>Answer</summary>

Add comment: `@agent-[N] claiming this task` and add label `claimed`
</details>

### 3. Progress Updates

**Q: How often must you update progress on in-progress tasks?**

<details>
<summary>Answer</summary>

Every 30 minutes
</details>

### 4. Finding Available Tasks

**Q: What GitHub filter finds unclaimed tasks?**

<details>
<summary>Answer</summary>

`is:open label:agent-task -label:claimed -label:in-progress`
</details>

### 5. Stale Task Authority

**Q: Who can mark tasks as stale?**

<details>
<summary>Answer</summary>

Any agent if timeout exceeded
</details>

### 6. Conflict Resolution

**Q: Two agents claim same task - who gets it?**

<details>
<summary>Answer</summary>

Earlier comment timestamp wins
</details>

### 7. Communication Protocol

**Q: Where do you communicate about task-specific issues?**

<details>
<summary>Answer</summary>

In GitHub Issue comments
</details>

### 8. Emergency Label

**Q: What label indicates urgent/blocking issues?**

<details>
<summary>Answer</summary>

`agent-urgent`
</details>

---

## Self-Assessment

**Score yourself:**
- 8/8 correct: ✅ Ready to claim tasks
- 6-7 correct: ⚠️ Re-read protocol sections you missed
- <6 correct: ❌ Re-read entire AGENT_PROTOCOL.md before proceeding

**If you can't answer all questions correctly, DO NOT claim any tasks until you re-read the protocol.**

---

## Browser Agent Specific

### Additional Verification for Comet Browser:

- [ ] I navigated to AGENT_PROTOCOL.md using browser tools
- [ ] I used `read_page` or `get_page_text` to read full content
- [ ] I checked /rules/ directory for domain guidelines
- [ ] I'm aware Space instructions don't auto-apply in browser
- [ ] I will check GitHub state before every action
- [ ] I will log my bootstrap in first issue comment

---

**Remember:** This verification isn't busy work - it prevents conflicts, wasted effort, and maintains multi-agent trust.
