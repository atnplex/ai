# Jules - Distributed AI Development System

A resilient, multi-node AI development assistant with centralized chat and distributed execution.

## Quick Start

```bash
# API Server (on oci-vps1)
cd api && uvicorn main:app --host 0.0.0.0 --port 8080

# Worker (on any node)
cd worker && python daemon.py
```

## Structure

```
jules/
├── api/           # FastAPI control plane
├── worker/        # Execution daemon
└── shared/        # Common models & utils
```

## Environment Variables

```bash
# Required (from Bitwarden)
GITHUB_TOKEN=          # GitHub PAT
REDIS_URL=             # Redis connection
BW_SESSION=            # Bitwarden session

# Optional
JULES_NODE_ID=         # Auto-detected from hostname
TAILSCALE_IP=          # Auto-detected
```
