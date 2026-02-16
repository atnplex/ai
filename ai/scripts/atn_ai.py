#!/usr/bin/env python3
import json
import asyncio
import asyncio.subprocess
import subprocess
import os
import sys
import argparse
from pathlib import Path

# --- Configuration ---
REGISTRY_PATH = Path("C:/atn/ai/ai/config/mcp_registry.json")

# --- Model Definitions ---
MODEL_ALIASES = {
    "sonnet": "claude-3-5-sonnet-20241022",
    "sonnet-thinking": "claude-3-5-sonnet-thinking",
    "opus": "claude-3-opus-20240229",
    "gemini-pro": "gemini-1.5-pro",
    "gemini-thinking": "gemini-2.0-flash-thinking",
    "openai-o1": "o1-preview",
    "openai-gpt4": "gpt-4o",
}


def log(msg):
    print(f"[atn-ai] {msg}")


async def run_mcp_task(server_name, prompt, model_alias=None):
    """Executes a prompt against an MCP server."""
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    server_cfg = registry["mcpServers"].get(server_name)
    if not server_cfg:
        return f"Error: Server {server_name} not found."

    # Map alias to full model ID if provided
    model_id = MODEL_ALIASES.get(model_alias, model_alias)

    cmd = [server_cfg["command"]] + server_cfg["args"]

    # --- Path Translation for Windows ---
    if os.name == "nt":
        # Translate /atn/ to C:/atn
        cmd = [c.replace("/atn/", "C:/atn/").replace("/atn", "C:/atn") for c in cmd]
        # If the command is a .sh file, wrap it in bash
        if cmd[0].endswith(".sh"):
            cmd = ["bash"] + cmd

    log(f"Dispatching to {server_name} [{model_id or 'default'}]...")

    try:
        # Prepare the Json-RPC call
        rpc_call = {
            "jsonrpc": "2.0",
            "method": "call_tool",
            "params": {
                "name": "ask",
                "arguments": {"prompt": prompt, "model": model_id},
            },
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
            return f"❌ {server_name} failed: {stderr.decode()}"

        return f"✅ {server_name} ({model_id}):\n{stdout.decode()}"
    except Exception as e:
        return f"⚠️ Exception in {server_name}: {str(e)}"


async def multi_model_orchestrator(prompt, selections):
    """
    selections: list of (server, model_alias) tuples
    """
    tasks = [run_mcp_task(srv, prompt, mod) for srv, mod in selections]
    results = await asyncio.gather(*tasks)
    return results


def main():
    parser = argparse.ArgumentParser(description="ATN Multi-Model Orchestrator")
    parser.add_argument("--prompt", required=True, help="Task or question")
    parser.add_argument(
        "--tier", choices=["speed", "thinking", "balanced"], default="balanced"
    )
    parser.add_argument(
        "--custom",
        help="Comma-sep list of server:model (e.g. anthropic:sonnet,gemini:pro)",
    )

    args = parser.parse_args()

    selections = []
    if args.custom:
        for item in args.custom.split(","):
            srv, mod = item.split(":")
            selections.append((srv, mod))
    else:
        # Default tier logic
        if args.tier == "thinking":
            selections = [
                ("anthropic", "sonnet-thinking"),
                ("gemini", "gemini-thinking"),
                ("openai", "openai-o1"),
            ]
        elif args.tier == "speed":
            selections = [("gemini", "gemini-pro"), ("anthropic", "sonnet")]
        else:
            selections = [("anthropic", "sonnet"), ("gemini", "gemini-pro")]

    log(f"Starting parallel job across {len(selections)} models...")
    results = asyncio.run(multi_model_orchestrator(args.prompt, selections))

    for res in results:
        print("\n" + "=" * 40)
        print(res)


if __name__ == "__main__":
    main()
