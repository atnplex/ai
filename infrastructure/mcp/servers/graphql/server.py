#!/usr/bin/env python3
"""
GraphQL MCP Server
Generic GraphQL query executor for any endpoint
"""

import json
from flask import Flask, jsonify, request
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from typing import Optional

app = Flask(__name__)

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "graphql-mcp"})

@app.route("/tool/query", methods=["POST"])
def execute_query():
    """Execute GraphQL query against specified endpoint"""
    data = request.json or {}
    
    endpoint = data.get("endpoint")
    query_str = data.get("query")
    variables = data.get("variables", {})
    headers = data.get("headers", {})
    
    if not endpoint or not query_str:
        return jsonify({"error": "endpoint and query required"}), 400
    
    try:
        # Setup transport with optional auth headers
        transport = RequestsHTTPTransport(
            url=endpoint,
            headers=headers,
            use_json=True
        )
        
        # Create client
        client = Client(transport=transport, fetch_schema_from_transport=False)
        
        # Execute query
        query = gql(query_str)
        result = client.execute(query, variable_values=variables)
        
        return jsonify({"data": result})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tool/introspect", methods=["POST"])
def introspect_schema():
    """Get GraphQL schema from endpoint"""
    data = request.json or {}
    
    endpoint = data.get("endpoint")
    headers = data.get("headers", {})
    
    if not endpoint:
        return jsonify({"error": "endpoint required"}), 400
    
    try:
        transport = RequestsHTTPTransport(
            url=endpoint,
            headers=headers,
            use_json=True
        )
        
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Get schema introspection
        introspection_query = gql("""
            query IntrospectionQuery {
                __schema {
                    queryType { name }
                    mutationType { name }
                    types {
                        name
                        kind
                        description
                    }
                }
            }
        """)
        
        result = client.execute(introspection_query)
        return jsonify({"schema": result})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9007, debug=False)
