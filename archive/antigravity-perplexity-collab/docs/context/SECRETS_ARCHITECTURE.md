# Secrets Architecture

> **Date**: 2026-02-03
> **Purpose**: Document the secure secrets management architecture

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                 Bitwarden Secrets Manager                    │
│                    (BWS - Master SSOT)                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              age-encrypted local cache                       │
│          ~/.config/atn/secrets/*.age                         │
│          ~/.atn/secrets/cache/*.age                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               Linux Kernel Keyring (keyctl)                  │
│                   In-memory only                             │
│               Auto-expires after TTL                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Environment Variables                           │
│           Passed to child processes                          │
│           NEVER logged or echoed                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Principles

| Principle | Implementation |
|-----------|----------------|
| **Never store secrets in plain text** | All secrets encrypted with age |
| **Never log secrets** | Use variables, pipe directly |
| **Never pass secrets as CLI args** | Visible in `ps aux` |
| **Decrypt → keyctl → export** | Secrets never touch shell variables during load |
| **Auto-expire** | keyctl TTL of 1 hour |
| **Offline-capable** | age-encrypted cache when BWS unavailable |

---

## Bootstrap Secret Flow

The BWS access token is the "master key" that unlocks everything else:

```bash
# 1. Token stored age-encrypted (done once)
echo -n "$BWS_ACCESS_TOKEN" | age -e -R recipients.txt > bws_token.age

# 2. At runtime: decrypt → pipe to keyctl (never touches variable)
age -d -i key.txt < bws_token.age | keyctl padd user "atn:BWS_ACCESS_TOKEN" @u

# 3. Read from keyctl when needed
BWS_ACCESS_TOKEN=$(keyctl pipe $key_id)
export BWS_ACCESS_TOKEN

# 4. Use BWS to fetch other secrets
bws secret get "GITHUB_PAT" | jq -r '.value'
```

---

## File Locations

| Path | Purpose | Permissions |
|------|---------|-------------|
| `~/.atn/secrets/age.key` | Private key for decryption | `600` |
| `~/.atn/secrets/recipients.txt` | Public key for encryption | `644` |
| `~/.config/atn/secrets/bws_token.age` | Encrypted BWS access token | `600` |
| `~/.atn/secrets/cache/*.age` | Encrypted secret cache | `600` |

---

## MCP Server Integration

Wrapper script: `/home/alex/.gemini/antigravity/scripts/mcp_with_secrets.sh`

Launches MCP servers with secrets from BWS:

```bash
# Instead of hardcoding in mcp_config.json:
mcp_with_secrets.sh npx @cloudflare/mcp-server-cloudflare

# The wrapper:
# 1. Loads BWS token from age → keyctl
# 2. Fetches required secrets based on MCP type
# 3. Exports to environment
# 4. Executes MCP server
```

---

## Current BWS Secrets

| Key | Purpose | Status |
|-----|---------|--------|
| `github` | GitHub PAT | ✅ Available |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account | ❓ To add |
| `CLOUDFLARE_API_TOKEN` | Cloudflare API | ❓ To add |
| `PERPLEXITY_API_KEY` | Perplexity API | ❓ To add |

---

## Rules Governing This

- **R69**: Secrets Management Standards
- **R70**: BWS Master Reference  
- **R71**: Secrets Encryption Required (NEW)

---

*Document created for Perplexity collaboration.*
