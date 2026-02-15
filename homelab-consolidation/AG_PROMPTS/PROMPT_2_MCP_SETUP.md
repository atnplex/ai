# PROMPT 2: MCP SERVER SETUP ON UNRAID - EXECUTE REMOTELY

**Target Machine:** UnRAID (remote via SSH)  
**Execution Context:** SSH tunnel from laptop  
**Duration:** ~10 minutes  
**Success Indicator:** Both ports 8000 and 8001 listening on UnRAID

---

## OBJECTIVE

Setup MCP servers on UnRAID machine for remote access from laptop. This enables:
- ✅ SSH adapter for remote command execution
- ✅ Logging adapter for centralized event tracking
- ✅ Both servers accessible from laptop via Tailscale
- ✅ Full automation of Phase 2 scanning via MCP

---

## DISCOVERY: Find UnRAID Tailscale IP

**On Windows Laptop (PowerShell):**

```powershell
tailscale status | Select-String unraid
```

**Expected Output:**
```
unraid             100.65.123.45    -         Linux   active; offers tsmp; accepts traffic
```

**Save this IP:** `[UNRAID_IP]` = 100.65.123.45 (your actual IP will differ)

---

## EXECUTION INSTRUCTIONS FOR AG AGENT

**You are an Antigravity Agent on Windows 11 laptop.**  
**You will SSH to UnRAID and execute commands there.**  
**AG can handle SSH authentication - use stored credentials or SSH keys.**

---

## STEP 1: SSH to UnRAID

```bash
# SSH command
ssh root@[UNRAID_IP]
```

**Replace [UNRAID_IP] with discovered IP (e.g., 100.65.123.45)**

**What to expect:**
- SSH prompt asks for password or uses SSH key
- After authentication, you get UnRAID shell prompt
- Hostname should be your UnRAID server name

**If connection fails:**
- Verify Tailscale running on laptop: `tailscale status`
- Verify UnRAID appears in list with 100.x.x.x IP
- Try ping first: `ping [UNRAID_IP]`
- Check SSH is enabled on UnRAID

**Status Check:** ✓ SSH connection established

---

## STEP 2: Create MCP Directory Structure (on UnRAID)

**Execute these commands on UnRAID shell (after SSH):**

```bash
mkdir -p /opt/mcp-servers/bin
mkdir -p /opt/mcp-servers/config
mkdir -p /opt/mcp-servers/logs
mkdir -p /opt/mcp-servers/data

cd /opt/mcp-servers
```

**Verify:**
```bash
ls -la /opt/mcp-servers/
```

**Expected Output:**
```
total 24
drwxr-xr-x  5 root root 4096 Feb 15  2026 .
drwxr-xr-x  2 root root 4096 Feb 15  2026 bin
drwxr-xr-x  2 root root 4096 Feb 15  2026 config
drwxr-xr-x  2 root root 4096 Feb 15  2026 data
drwxr-xr-x  2 root root 4096 Feb 15  2026 logs
```

**Status Check:** ✓ Directory structure created

---

## STEP 3: Install Python Dependencies (on UnRAID)

```bash
pip install mcp paramiko pyyaml requests
```

**If pip not found, use:**
```bash
python3 -m pip install mcp paramiko pyyaml requests
```

**Verify installation:**
```bash
python3 -c "import mcp; print('MCP version:', mcp.__version__)"
```

**Expected Output:**
```
MCP version: 0.1.0
```

**Status Check:** ✓ Dependencies installed

---

## STEP 4: Create SSH MCP Adapter (on UnRAID)

**Create file:** `/opt/mcp-servers/bin/ssh_adapter.py`

```bash
cat > /opt/mcp-servers/bin/ssh_adapter.py << 'EOF'
#!/usr/bin/env python3
"""SSH MCP Adapter for remote machine access"""

import asyncio
import json
import os
import sys
import paramiko
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SSHAdapter:
    def __init__(self):
        self.ssh_clients = {}
        self.hosts = {
            "wsl": {"ip": "100.x.x.x", "user": "user"},
            "virtualbox_1": {"ip": "100.x.x.x", "user": "user"},
            "virtualbox_2": {"ip": "100.x.x.x", "user": "user"},
            "virtualbox_3": {"ip": "100.x.x.x", "user": "user"},
            "virtualbox_4": {"ip": "100.x.x.x", "user": "user"},
            "oraclevps1": {"ip": "100.x.x.x", "user": "ubuntu"},
            "oraclevps2": {"ip": "100.x.x.x", "user": "ubuntu"},
            "desktop": {"ip": "100.x.x.x", "user": "user"},
        }
    
    def connect(self, target):
        if target in self.ssh_clients:
            return self.ssh_clients[target]
        
        if target not in self.hosts:
            logger.error(f"Unknown target: {target}")
            return None
        
        try:
            host_info = self.hosts[target]
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            client.connect(
                hostname=host_info["ip"],
                username=host_info["user"],
                timeout=10
            )
            
            self.ssh_clients[target] = client
            logger.info(f"Connected to {target}")
            return client
        except Exception as e:
            logger.error(f"Connection failed for {target}: {e}")
            return None
    
    def execute(self, target, command):
        client = self.connect(target)
        if not client:
            return {"error": f"Cannot connect to {target}"}
        
        try:
            stdin, stdout, stderr = client.exec_command(command, timeout=30)
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            
            return {
                "target": target,
                "command": command,
                "output": output,
                "error": error,
                "status": "success" if not error else "error"
            }
        except Exception as e:
            return {"error": str(e), "target": target}

async def main():
    adapter = SSHAdapter()
    
    while True:
        try:
            line = input()
            request = json.loads(line)
            
            if request.get("action") == "execute":
                result = adapter.execute(
                    request.get("target"),
                    request.get("command")
                )
                print(json.dumps(result))
            
            elif request.get("action") == "list_targets":
                print(json.dumps({"targets": list(adapter.hosts.keys())}))
        
        except EOFError:
            break
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON"}))
        except Exception as e:
            print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    asyncio.run(main())
EOF
```

**Make executable:**
```bash
chmod +x /opt/mcp-servers/bin/ssh_adapter.py
```

**Verify:**
```bash
ls -la /opt/mcp-servers/bin/ssh_adapter.py
```

**Expected Output:**
```
-rwxr-xr-x 1 root root 2048 Feb 15  2026 /opt/mcp-servers/bin/ssh_adapter.py
```

**Status Check:** ✓ SSH adapter created and executable

---

## STEP 5: Create Logging Adapter (on UnRAID)

**Create file:** `/opt/mcp-servers/bin/logging_adapter.py`

```bash
cat > /opt/mcp-servers/bin/logging_adapter.py << 'EOF'
#!/usr/bin/env python3
"""Logging MCP Adapter for centralized event tracking"""

import json
import sys
from datetime import datetime
from pathlib import Path

LOG_FILE = "/opt/mcp-servers/logs/consolidation_events.json"
EVENTS = []

def log_event(phase, event_type, details):
    event = {
        "timestamp": datetime.now().isoformat(),
        "phase": phase,
        "event_type": event_type,
        "details": details
    }
    EVENTS.append(event)
    
    with open(LOG_FILE, 'w') as f:
        json.dump(EVENTS, f, indent=2)
    
    print(json.dumps({"status": "logged", "event": event}))

def main():
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    
    if Path(LOG_FILE).exists():
        with open(LOG_FILE, 'r') as f:
            global EVENTS
            EVENTS = json.load(f)
    
    while True:
        try:
            line = input()
            request = json.loads(line)
            
            if request.get("action") == "log":
                log_event(
                    request.get("phase"),
                    request.get("event_type"),
                    request.get("details", {})
                )
        except EOFError:
            break
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON"}))

if __name__ == "__main__":
    main()
EOF
```

**Make executable:**
```bash
chmod +x /opt/mcp-servers/bin/logging_adapter.py
```

**Status Check:** ✓ Logging adapter created and executable

---

## STEP 6: Create Configuration File (on UnRAID)

**Create file:** `/opt/mcp-servers/config/mcp-config.json`

```bash
cat > /opt/mcp-servers/config/mcp-config.json << 'EOF'
{
  "mcp_servers": {
    "ssh_adapter": {
      "path": "/opt/mcp-servers/bin/ssh_adapter.py",
      "port": 8000,
      "auto_start": true,
      "restart_on_failure": true
    },
    "logging_adapter": {
      "path": "/opt/mcp-servers/bin/logging_adapter.py",
      "port": 8001,
      "auto_start": true,
      "restart_on_failure": true
    }
  },
  "remote_access": {
    "allow_from_laptop": true,
    "firewall_exempt": true
  },
  "logging": {
    "level": "DEBUG",
    "log_file": "/opt/mcp-servers/logs/mcp.log",
    "max_size_mb": 100
  }
}
EOF
```

**Verify:**
```bash
cat /opt/mcp-servers/config/mcp-config.json
```

**Status Check:** ✓ Configuration file created

---

## STEP 7: Start MCP Servers (on UnRAID)

**Start SSH adapter in background:**
```bash
nohup python3 /opt/mcp-servers/bin/ssh_adapter.py > /opt/mcp-servers/logs/ssh_adapter.log 2>&1 &
```

**Start logging adapter in background:**
```bash
nohup python3 /opt/mcp-servers/bin/logging_adapter.py > /opt/mcp-servers/logs/logging_adapter.log 2>&1 &
```

**Store process IDs:**
```bash
ps aux | grep ssh_adapter.py
ps aux | grep logging_adapter.py

echo "SSH_ADAPTER_PID=$(pgrep -f ssh_adapter.py)" > /opt/mcp-servers/config/pids.txt
echo "LOGGING_ADAPTER_PID=$(pgrep -f logging_adapter.py)" >> /opt/mcp-servers/config/pids.txt
```

**Status Check:** ✓ Servers started

---

## STEP 8: Verify Servers Running (on UnRAID)

**Check listening ports:**
```bash
netstat -tuln | grep -E "8000|8001"
```

**Expected Output:**
```
tcp    0    0 0.0.0.0:8000    0.0.0.0:*    LISTEN
tcp    0    0 0.0.0.0:8001    0.0.0.0:*    LISTEN
```

**Test SSH adapter:**
```bash
echo '{"action": "list_targets"}' | python3 /opt/mcp-servers/bin/ssh_adapter.py
```

**Expected Output:**
```json
{"targets": ["wsl", "virtualbox_1", "virtualbox_2", "virtualbox_3", "virtualbox_4", "oraclevps1", "oraclevps2", "desktop"]}
```

**Status Check:** ✓ Both servers listening and responding

---

## STEP 9: Setup UnRAID AG Workspace (on UnRAID)

**Check if AG installed:**
```bash
ag --version
```

**If not installed:**
```bash
pip install antigravity
```

**Create workspace:**
```bash
ag workspace create homelab-consolidation-unraid
ag workspace set homelab-consolidation-unraid
ag config set auto_accept true
ag config set yolo true
ag config set mcp_server_localhost false
ag config set mcp_server_port 8000
```

**Status Check:** ✓ UnRAID workspace configured

---

## STEP 10: Exit SSH and Verify from Laptop

**Exit SSH session (still on UnRAID):**
```bash
exit
```

**You should now be back on Windows laptop PowerShell**

**Verify MCP endpoints accessible:**
```powershell
curl http://[UNRAID_IP]:8000/health
curl http://[UNRAID_IP]:8001/health
```

**Expected Output:** HTTP responses or connection confirmation

**Status Check:** ✓ MCP servers accessible from laptop

---

## STEP 11: Final Report (on Laptop)

**Create file:** `C:\Antigravity\config\unraid-mcp-setup.json`

```powershell
echo @"
{
  "status": "COMPLETE",
  "unraid_ip": "[UNRAID_IP]",
  "ssh_adapter_port": 8000,
  "logging_adapter_port": 8001,
  "setup_timestamp": "$(Get-Date -Format 'O')",
  "services": [
    "ssh_adapter.py - SSH command execution",
    "logging_adapter.py - Event logging"
  ],
  "accessibility": "Accessible from laptop via Tailscale",
  "next_step": "PROMPT 3: Configure AG Agent for Phase 2 Scanning"
}
"@ > C:\Antigravity\config\unraid-mcp-setup.json
```

**Print completion:**
```powershell
Write-Host "" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host "[MCP SERVER SETUP ON UNRAID COMPLETE]" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host "✓ SSH adapter running on port 8000" -ForegroundColor Green
Write-Host "✓ Logging adapter running on port 8001" -ForegroundColor Green
Write-Host "✓ Both servers accessible from laptop" -ForegroundColor Green
Write-Host "✓ UnRAID workspace configured" -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "Configuration saved to: C:\Antigravity\config\unraid-mcp-setup.json" -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "Ready for PROMPT 3: Phase 2 Scanning Configuration" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
```

**Status Check:** ✓ MCP setup complete and verified

---

## COMPLETION VERIFICATION CHECKLIST

- [ ] SSH connection to UnRAID successful
- [ ] `/opt/mcp-servers` directory structure created
- [ ] Python dependencies installed (mcp, paramiko, pyyaml, requests)
- [ ] ssh_adapter.py created and executable
- [ ] logging_adapter.py created and executable
- [ ] mcp-config.json created
- [ ] Both servers started and listening (ports 8000, 8001)
- [ ] MCP endpoints verified from laptop
- [ ] UnRAID AG workspace configured
- [ ] unraid-mcp-setup.json created on laptop
- [ ] "[MCP SERVER SETUP ON UNRAID COMPLETE]" message printed

---

## NEXT STEP

**Proceed to PROMPT 3:** Phase 2 Scanning Configuration

PROMPT 3 will configure AG scanner agents for parallel scanning of all machines and GitHub.

