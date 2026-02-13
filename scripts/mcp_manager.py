#!/usr/bin/env python3
import json
import os
import sys
import argparse
from pathlib import Path

# Paths
BASE_DIR = Path("/atn/ai")
REGISTRY_FILE = BASE_DIR / "config/mcp_registry.json"
CONFIG_FILE = BASE_DIR / "config/mcp_config.json"


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Updated {path}")


def get_registry():
    if not REGISTRY_FILE.exists():
        print(f"Error: Registry file not found at {REGISTRY_FILE}")
        sys.exit(1)
    return load_json(REGISTRY_FILE)


def get_config():
    return load_json(CONFIG_FILE)


def list_servers():
    registry = get_registry()
    config = get_config()

    enabled_servers = set(config.get("mcpServers", {}).keys())
    all_servers = sorted(registry.get("mcpServers", {}).keys())

    print(f"{'SERVER NAME':<30} {'STATUS':<10}")
    print("-" * 40)
    for server in all_servers:
        status = "ENABLED" if server in enabled_servers else "DISABLED"
        print(f"{server:<30} {status:<10}")


def enable_server(server_name):
    registry = get_registry()
    config = get_config()

    if server_name not in registry.get("mcpServers", {}):
        print(f"Error: Server '{server_name}' not found in registry.")
        return

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    config["mcpServers"][server_name] = registry["mcpServers"][server_name]
    save_json(CONFIG_FILE, config)
    print(f"Enabled '{server_name}'")


def disable_server(server_name):
    config = get_config()

    if server_name in config.get("mcpServers", {}):
        del config["mcpServers"][server_name]
        save_json(CONFIG_FILE, config)
        print(f"Disabled '{server_name}'")
    else:
        print(f"Server '{server_name}' is already disabled or not configured.")


def reset_to_defaults():
    registry = get_registry()
    defaults = registry.get("defaults", [])

    new_config = {"mcpServers": {}}
    for server in defaults:
        if server in registry["mcpServers"]:
            new_config["mcpServers"][server] = registry["mcpServers"][server]

    save_json(CONFIG_FILE, new_config)
    print(f"Reset configuration to defaults: {', '.join(defaults)}")


def main():
    parser = argparse.ArgumentParser(description="Manage MCP servers")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list", help="List all available servers and their status")

    enable_parser = subparsers.add_parser("enable", help="Enable a server")
    enable_parser.add_argument("server", help="Name of the server to enable")

    disable_parser = subparsers.add_parser("disable", help="Disable a server")
    disable_parser.add_argument("server", help="Name of the server to disable")

    subparsers.add_parser("reset", help="Reset configuration to defaults")

    args = parser.parse_args()

    if args.command == "list":
        list_servers()
    elif args.command == "enable":
        enable_server(args.server)
    elif args.command == "disable":
        disable_server(args.server)
    elif args.command == "reset":
        reset_to_defaults()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
