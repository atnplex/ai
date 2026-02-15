# PROMPT 1: GLOBAL AUTOMATION SETUP - EXECUTE ON LAPTOP

**Target Machine:** Windows 11 Laptop  
**Execution Context:** Local (AG running on this machine)  
**Duration:** ~5 minutes  
**Success Indicator:** "[GLOBAL AUTOMATION SETUP COMPLETE]" in output

---

## OBJECTIVE

Configure AG workspace for complete automation and agent-command support globally. This enables:
- ✅ Auto-accept of all agent commands
- ✅ YOLO mode (no confirmations)
- ✅ Remote agent execution
- ✅ Cross-workspace command execution
- ✅ Automatic API routing to appropriate models
- ✅ Centralized logging and telemetry

---

## EXECUTION INSTRUCTIONS FOR AG AGENT

**You are an Antigravity Agent running on Windows 11 laptop.**  
**These are your direct orders. Execute exactly as written.**  
**Report completion status after each major section.**

---

## STEP 1: Global Configuration - Auto-Accept All Agent Commands

```powershell
ag config set auto_accept true
ag config set auto_accept_timeout 300
ag config set yolo true
ag config set parallel_agents 4
ag config set agent_command_require_approval false
ag config set workspace_isolation false
```

**Verification:**
```powershell
ag config show
```

**Expected Output:**
```
auto_accept: true
auto_accept_timeout: 300
yolo: true
parallel_agents: 4
agent_command_require_approval: false
workspace_isolation: false
```

**Status Check:** ✓ All settings configured

---

## STEP 2: Enable Remote Agent Execution

```powershell
ag config set remote_agent_execution true
ag config set remote_agent_auto_spawn true
ag config set remote_agent_ssh_tunnel true
ag config set remote_agent_firewall_exempt true
```

**Verification:**
```powershell
ag config show | Select-String remote
```

**Expected Output:**
```
remote_agent_execution: true
remote_agent_auto_spawn: true
remote_agent_ssh_tunnel: true
remote_agent_firewall_exempt: true
```

**Status Check:** ✓ Remote execution enabled

---

## STEP 3: Setup Agent-to-Agent Communication

```powershell
ag config set agent_communication_protocol grpc
ag config set agent_communication_encryption true
ag config set agent_communication_broadcast_mode true
ag config set agent_communication_timeout 600
```

**Status Check:** ✓ Agent communication configured

---

## STEP 4: Enable Cross-Workspace Commands

```powershell
ag config set cross_workspace_execution true
ag config set cross_workspace_auth disabled
ag config set cross_workspace_logging true
ag config set cross_workspace_broadcast true
```

**Status Check:** ✓ Cross-workspace execution enabled

---

## STEP 5: Workspace-Specific Settings

```powershell
ag workspace config homelab-consolidation set auto_accept true
ag workspace config homelab-consolidation set agent_override_enabled true
ag workspace config homelab-consolidation set agent_command_queue_enabled true
ag workspace config homelab-consolidation set agent_command_queue_max_size 100
```

**Status Check:** ✓ Workspace configured

---

## STEP 6: Create Master Agent Profile

**Create file:** `C:\Antigravity\profiles\consolidation-master.json`

```json
{
  "profile_name": "consolidation-master",
  "description": "Master orchestrator for homelab consolidation",
  "capabilities": {
    "auto_accept_commands": true,
    "yolo_mode": true,
    "parallel_execution": 4,
    "remote_execution": true,
    "cross_workspace": true,
    "agent_spawning": true,
    "mcp_control": true
  },
  "permissions": {
    "filesystem": true,
    "network": true,
    "process": true,
    "system": true,
    "agent_management": true,
    "api_access": true
  },
  "rules": {
    "require_approval": false,
    "require_confirmation": false,
    "broadcast_commands": true,
    "auto_retry": true,
    "retry_count": 3
  }
}
```

**Status Check:** ✓ Master profile created

---

## STEP 7: Apply Master Profile

```powershell
ag profile apply consolidation-master
ag profile set-default consolidation-master
```

**Verification:**
```powershell
ag profile show current
ag profile show consolidation-master
```

**Status Check:** ✓ Master profile applied as default

---

## STEP 8: Enable API Routing

```powershell
ag config set api_routing_enabled true
ag config set api_claude_enabled true
ag config set api_gemini_enabled true
ag config set api_gpt_enabled true
ag config set api_perplexity_enabled true
```

**Create file:** `C:\Antigravity\config\api-routing.json`

```json
{
  "routing": {
    "default": "claude",
    "claude_opus_4_6": {
      "api_endpoint": "https://api.anthropic.com",
      "model": "claude-opus-4-1-20250805",
      "use_for": ["reasoning", "consolidation", "synthesis"],
      "auto_route": true
    },
    "gemini_pro_3": {
      "api_endpoint": "https://generativelanguage.googleapis.com",
      "model": "gemini-pro-3-thinking",
      "use_for": ["data_structures", "filesystem", "github"],
      "auto_route": true
    },
    "gpt_5_2": {
      "api_endpoint": "https://api.openai.com",
      "model": "gpt-5.2-preview",
      "use_for": ["long_context", "integration", "ssh"],
      "auto_route": true
    },
    "perplexity_pro": {
      "api_endpoint": "https://api.perplexity.ai",
      "model": "sonar-pro",
      "use_for": ["documentation", "best_practices"],
      "auto_route": true
    }
  }
}
```

**Status Check:** ✓ API routing configured

---

## STEP 9: Enable Logging and Telemetry

```powershell
ag config set logging_level debug
ag config set telemetry_enabled true
ag config set event_logging_enabled true
ag config set command_audit_trail true

# Create logging directories
mkdir C:\Antigravity\logs\consolidation
mkdir C:\Antigravity\logs\agents
mkdir C:\Antigravity\logs\commands
```

**Status Check:** ✓ Logging configured

---

## STEP 10: Verification and Final Report

```powershell
# Dump all config settings
ag config show > C:\Antigravity\config\setup_complete.json
ag profile show consolidation-master >> C:\Antigravity\config\setup_complete.json

# Print completion status
Write-Host "" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host "[GLOBAL AUTOMATION SETUP COMPLETE]" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host "✓ Auto-accept enabled globally" -ForegroundColor Green
Write-Host "✓ YOLO mode enabled globally" -ForegroundColor Green
Write-Host "✓ Remote agent execution enabled" -ForegroundColor Green
Write-Host "✓ Cross-workspace execution enabled" -ForegroundColor Green
Write-Host "✓ API routing configured" -ForegroundColor Green
Write-Host "✓ Logging configured" -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "Configuration saved to: C:\Antigravity\config\setup_complete.json" -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "Ready for PROMPT 2: MCP Server Setup on UnRAID" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
```

**Status Check:** ✓ All configurations verified and saved

---

## COMPLETION VERIFICATION CHECKLIST

Before moving to PROMPT 2, verify all items:

- [ ] All ag config commands executed without error
- [ ] consolidation-master profile created in `C:\Antigravity\profiles\`
- [ ] consolidation-master set as default profile
- [ ] API routing configured in `C:\Antigravity\config\api-routing.json`
- [ ] Log directories created (consolidation, agents, commands)
- [ ] setup_complete.json generated with all settings
- [ ] "[GLOBAL AUTOMATION SETUP COMPLETE]" message printed

---

## NEXT STEP

**Proceed to PROMPT 2:** MCP Server Setup on UnRAID

PROMPT 2 will SSH to UnRAID and configure MCP servers for remote access.

