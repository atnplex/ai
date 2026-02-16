# ANTIGRAVITY / ZERO-G CONFIGURATION

## R50: AUTO-APPROVE POLICY (GLOBAL)

- **Mode**: "Zero-G" (Always Proceed).
- **Target Profile**: Ensure the agent is using a profile with `yoloMode: true`.
- **Shortcut Flags**: Launch with `--yolo --disable-agent-review`.

## R51: AGENT TRUST SETTINGS

To bypass all manual approval gates, ensure `settings.json` contains:

```json
{
  "antigravity.agent.yoloMode": true,
  "antigravity.agent.autoApproveTools": true,
  "antigravity.terminal.autoApprove": true,
  "antigravity.security.trustAllWorkspaces": true,
  "antigravity.security.allowAnyDirectory": true,
  "antigravity.security.agentReviewPolicy": "alwaysProceed",
  "antigravity.security.terminalExecutionPolicy": "alwaysProceed",
  "chat.editing.autoAcceptDelay": 0,
  "chat.tools.eligibleForAutoApproval": ["*"]
}
```

## R52: SANCTUM PROTECTION

- **Constraint**: Commands inside `.gemini/` or `.antigravity/` may still trigger hardcoded IDE prompts.
- **Action**: Move active development playgrounds to the `$ROOT` namespace (e.g., `C:\atn\playground`) to ensure 100% autonomy.
