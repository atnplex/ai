# ⚠️ CRITICAL: Comet Browser Agent Bootstrap

**Version:** 1.0  
**Last Updated:** 2026-02-13  
**Status:** MANDATORY for all browser-based agents

---

## 🚨 READ THIS FIRST

If you are operating through **Comet Browser** (not the Perplexity web UI), you MUST complete this bootstrap process before taking ANY actions.

**Why?** Perplexity Space custom instructions do NOT automatically apply to browser automation sessions. You must manually enforce protocol compliance.

---

## Mandatory Bootstrap Steps

### Before EVERY browser session:

**1. Navigate to Protocol Documentation**
```
github.com/atnplex/ai/.comet-browser/AGENT_PROTOCOL.md
```
- Use `read_page` or `get_page_text` to read FULL protocol
- Do NOT skip sections
- Do NOT assume you remember from previous sessions

**2. Read Domain Guidelines**
```
github.com/atnplex/ai/rules/
```
- Check for new or updated rules
- Read all .md files in rules directory
- Note any domain-specific constraints

**3. Self-Verify Understanding**
```
github.com/atnplex/ai/.comet-browser/VERIFICATION_CHECKLIST.md
```
- Answer verification questions
- If you can't answer, re-read protocol
- Do NOT proceed until verified

**4. Check for Urgent Issues**
```
GitHub Issues filter: is:open label:agent-urgent
```
- Address any urgent/blocking issues first
- Read all comments on urgent issues
- Coordinate with other agents if needed

**5. Find Available Tasks**
```
GitHub Issues filter: is:open label:agent-task -label:claimed -label:in-progress
```
- Verify no other agent has claimed your target task
- Check timestamps on all comments
- Review task description and requirements

---

## Identity Declaration

Before claiming any task, declare your agent identity in your first comment:
```
@agent-[1/2/3] bootstrap complete, claiming this task
```

Replace [1/2/3] with your assigned agent number.

---

## ❌ DO NOT Skip Bootstrap

**Consequences of skipping:**
- Protocol violations logged in GitHub
- Conflicts with other agents
- Stale tasks and wasted work
- Trust degradation in multi-agent system

**All actions are logged.** Other agents can see if you skip protocol steps.

---

## Browser Context Awareness

### Key Differences: Browser vs. Web UI

| Aspect | Perplexity Web UI | Comet Browser |
|--------|-------------------|---------------|
| Custom Instructions | ✅ Automatically applied | ❌ Manual enforcement required |
| Space Context | ✅ Always available | ❌ Must navigate manually |
| Protocol Adherence | ✅ Prompted by Space | ❌ Self-disciplined only |
| State Tracking | ✅ In conversation | ❌ Must check GitHub each time |

**Bottom line:** Browser automation = Manual bootstrap EVERY time.

---

## Session Start Template

Copy and use this checklist at the start of each session:

```markdown
## Session Bootstrap Checklist
- [ ] Read AGENT_PROTOCOL.md (use browser tools)
- [ ] Check /rules/ directory for updates
- [ ] Complete VERIFICATION_CHECKLIST.md
- [ ] Identify as @agent-[N]
- [ ] Check for agent-urgent issues
- [ ] Review my active tasks (assignee:@me)
- [ ] Find available task (proper filter)
- [ ] Verified no conflicts with other agents
- [ ] Ready to claim and execute
```

---

## Automation Best Practices

1. **Always use browser tools explicitly:**
   - `navigate` to protocol docs
   - `read_page` to consume full content
   - `get_page_text` for long documents
   - Never assume cached knowledge

2. **Log your bootstrap:**
   - Add comment to first issue you work on
   - Include: "Bootstrap complete [timestamp]"
   - Shows other agents you followed protocol

3. **Check before every action:**
   - Task state can change between browser requests
   - Another agent may have claimed while you were reading
   - Always verify current state before modifying

---

## Emergency Override

If GitHub is down or protocol docs are inaccessible:
1. **DO NOT PROCEED** with any task work
2. Create issue with label `agent-urgent` when GitHub recovers
3. Document what you attempted to do
4. Wait for system recovery

**Never work without access to SSOT.**

---

## Questions?

If this bootstrap process is unclear:
1. Create issue with label `agent-urgent`
2. Tag: `@agent-1 @agent-2 @agent-3`
3. Wait for clarification
4. Do NOT guess or skip steps

---

**Remember:** This protocol exists to prevent conflicts and ensure coordination. Following it protects all agents and maintains system integrity.
