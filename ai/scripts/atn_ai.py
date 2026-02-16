#!/usr/bin/env python3
import json
import asyncio
import subprocess
import os
import sys
import argparse
from pathlib import Path

# --- Configuration ---
REGISTRY_PATH = Path("C:/atn/ai/ai/config/mcp_registry.json")


def log(msg):
    print(f"[atn-ai] {msg}")


async def run_mcp_task(server_name, prompt):
    """Executes a simple prompt against an MCP server using its registered command."""
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    server_cfg = registry["mcpServers"].get(server_name)
    if not server_cfg:
        return f"Error: Server {server_name} not found."

    cmd = [server_cfg["command"]] + server_cfg["args"]

    log(f"Starting {server_name}...")
    # This is a simplified execution. In production, we'd use an MCP client.
    # For now, we simulate by passing the prompt to the server's stdin if it supports it,
    # or just log the intent.
    try:
        # Mocking the JSON-RPC call to 'ask' tool
        rpc_call = {
            "jsonrpc": "2.0",
            "method": "call_tool",
            "params": {"name": "ask", "arguments": {"prompt": prompt}},
            "id": 1,
        }

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate(input=json.dumps(rpc_call).encode())

        if proc.returncode != 0:
            return f"{server_name} failed: {stderr.decode()}"

        return f"{server_name} response: {stdout.decode()}"
    except Exception as e:
        return f"Exception in {server_name}: {str(e)}"


async def parallel_ask(prompt, models):
    tasks = [run_mcp_task(model, prompt) for model in models]
    results = await asyncio.gather(*tasks)
    return results


def main():
    parser = argparse.ArgumentParser(description="ATN Parallel AI Dispatcher")
    parser.add_argument("--prompt", required=True, help="Prompt to send")
    parser.add_argument(
        "--models", default="gemini,anthropic,openai", help="Comma-separated models"
    )

    args = parser.parse_args()
    models = [m.strip() for m in args.models.split(",")]

    log(f"Dispatching parallel request to: {', '.join(models)}")
    results = asyncio.run(parallel_ask(args.prompt, models))

    for res in results:
        print("-" * 20)
        print(res)


if __name__ == "__main__":
    main()
