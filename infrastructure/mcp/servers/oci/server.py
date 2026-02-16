#!/usr/bin/env python3
"""
OCI CLI MCP Server
Provides SSE transport for Oracle Cloud Infrastructure CLI operations
"""

import os
import subprocess
import json
from flask import Flask, Response, jsonify, request
from typing import Generator, Optional, List

app = Flask(__name__)

OCI_CONFIG_FILE = os.getenv("OCI_CONFIG_FILE", "/root/.oci/config")
OCI_PROFILE = os.getenv("OCI_PROFILE", "DEFAULT")

def run_oci_command(args: List[str]) -> dict:
    """Run OCI CLI command and return JSON output"""
    cmd = ["oci"] + args + ["--config-file", OCI_CONFIG_FILE, "--profile", OCI_PROFILE, "--output", "json"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"OCI CLI error: {result.stderr}")
    
    return json.loads(result.stdout) if result.stdout else {}

@app.route("/health")
def health():
    """Health check endpoint"""
    try:
        # Test OCI CLI availability
        subprocess.run(["oci", "--version"], capture_output=True, check=True)
        return jsonify({"status": "healthy", "service": "oci-mcp"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

@app.route("/tool/list_instances", methods=["POST"])
def list_instances():
    """List compute instances in compartment"""
    data = request.json or {}
    compartment_id = data.get("compartment_id")
    
    if not compartment_id:
        return jsonify({"error": "compartment_id required"}), 400
    
    try:
        result = run_oci_command(["compute", "instance", "list", "-c", compartment_id])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tool/start_instance", methods=["POST"])
def start_instance():
    """Start a stopped instance"""
    data = request.json or {}
    instance_id = data.get("instance_id")
    
    if not instance_id:
        return jsonify({"error": "instance_id required"}), 400
    
    try:
        result = run_oci_command(["compute", "instance", "action", "--action", "START", "--instance-id", instance_id])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tool/stop_instance", methods=["POST"])
def stop_instance():
    """Stop a running instance"""
    data = request.json or {}
    instance_id = data.get("instance_id")
    
    if not instance_id:
        return jsonify({"error": "instance_id required"}), 400
    
    try:
        result = run_oci_command(["compute", "instance", "action", "--action", "STOP", "--instance-id", instance_id])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tool/list_compartments", methods=["POST"])
def list_compartments():
    """List compartments in tenancy"""
    data = request.json or {}
    tenancy_id = data.get("tenancy_id")
    
    if not tenancy_id:
        return jsonify({"error": "tenancy_id required"}), 400
    
    try:
        result = run_oci_command(["iam", "compartment", "list", "-c", tenancy_id, "--all"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9006, debug=False)
