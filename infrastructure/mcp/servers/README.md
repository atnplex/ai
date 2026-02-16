# Custom MCP Servers

This directory is for custom MCP server implementations.

Currently, all MCP servers are sourced from upstream packages (Docker images or npm).
When you need a custom server, add its code here following MCP protocol standards.

## Creating a Custom Server

1. Create a subdirectory: `servers/<name>/`
2. Implement the MCP stdio transport protocol
3. Add the server to `ai/config/mcp_registry.json`
4. Add registry metadata to `registry/servers.yaml`
5. Run `python3 /atn/ai/scripts/mcp_manager.py generate` to update the config

## Reference

- [MCP Specification](https://modelcontextprotocol.io/specification)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
