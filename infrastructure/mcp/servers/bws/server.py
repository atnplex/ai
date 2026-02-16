#!/usr/bin/env python3
"""
BWS MCP Server
Provides SSE transport for Bitwarden Secrets Manager operations
"""

import os
import subprocess
import json
from flask import Flask, Response, jsonify, request
from typing import Generator, Optional

app = Flask(__name__)

BWS_ACCESS_TOKEN = os.getenv("BWS_ACCESS_TOKEN")

def get_secret(secret_id: str) -> str:
    """Fetch a secret from BWS"""
    if not BWS_ACCESS_TOKEN:
        raise ValueError("BWS_ACCESS_TOKEN not set")
    
    result = subprocess.run(
        ["bws", "secret", "get", secret_id, "--access-token", BWS_ACCESS_TOKEN],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"BWS error: {result.stderr}")
    
    data = json.loads(result.stdout)
    return data.get("value", "")

def list_secrets(project_id: Optional[str] = None) -> list:
    """List all secrets, optionally filtered by project"""
    cmd = ["bws", "secret", "list", "--access-token", BWS_ACCESS_TOKEN]
    if project_id:
        cmd.extend(["--project-id", project_id])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"BWS error: {result.stderr}")
    
    return json.loads(result.stdout)

@app.route("/health")
def health():
    """Health check endpoint"""
    try:
        # Test BWS connectivity
        subprocess.run(
            ["bws", "--version"],
            capture_output=True,
            check=True
        )
        return jsonify({"status": "healthy", "service": "bws-mcp"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

@app.route("/sse")
def sse():
    """SSE endpoint for MCP protocol"""
    def event_stream() -> Generator:
        # MCP initialization
        yield f"data: {json.dumps({'type': 'init', 'tools': ['get_secret', 'list_secrets']})}\n\n"
        
        # Listen for tool invocations
        while True:
            # In production, this would use a queue/websocket for bi-directional communication
            # For now, return available tools
            yield f"data: {json.dumps({'type': 'ready'})}\n\n"
            break
    
    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/tool/<tool_name>", methods=["POST"])
def invoke_tool(tool_name: str):
    """HTTP endpoint for tool invocation (alternative to SSE)"""
    data = request.json
    
    try:
        if tool_name == "get_secret":
            secret_id = data.get("secret_id")
            if not secret_id:
                return jsonify({"error": "secret_id required"}), 400
            value = get_secret(secret_id)
            return jsonify({"value": value})
        
        elif tool_name == "list_secrets":
            project_id = data.get("project_id")
            secrets = list_secrets(project_id)
            return jsonify({"secrets": secrets})
        
        else:
            return jsonify({"error": f"Unknown tool: {tool_name}"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    if not BWS_ACCESS_TOKEN:
        print("ERROR: BWS_ACCESS_TOKEN environment variable not set")
        exit(1)
    
    app.run(host="0.0.0.0", port=9000, debug=False)
