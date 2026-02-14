# atnplex/ai

Single Source of Truth (SSOT) for AI agent coordination, protocols, and configuration across the atnplex organization.

## Repository Structure

| Directory                          | Purpose                                              |
|-----------------------------------|------------------------------------------------------|
| [.comet-browser/](.comet-browser/) | Perplexity Multi-Agent Coordination System           |
| [rules/](rules/)                   | Operational rules (MCP management, state validation) |
| [config/](config/)                 | MCP server registry                                  |
| [scripts/](scripts/)               | Utilities (sync, MCP manager, secrets)               |
| [.github/](.github/)               | Issue templates, PR template, CODEOWNERS             |

## Quick Start

1. Read [AGENT_PROTOCOL.md](.comet-browser/AGENT_PROTOCOL.md) — core coordination protocol
2. Check [PROTOCOL_VERSION](PROTOCOL_VERSION) — current version
3. Derive your agent ID using the formula in the protocol: `{platform}-{profile}`

## Protocol Version

Current version: see [PROTOCOL_VERSION](PROTOCOL_VERSION)
