from fastmcp import FastMCP
import requests
import json
import os

NODE_RED_URL = os.environ.get("NODE_RED_URL")

mcp = FastMCP("node-red")

@mcp.tool()
def get_flows():
    """Get all node-red flows as json"""
    return requests.get(f"{NODE_RED_URL}/flows").text

@mcp.tool()
def update_flows(flows: str) -> str:
    """Replace all node-red flows with provided json"""
    r = requests.post(f"{NODE_RED_URL}/flows", data=flows, headers={"Content-Type": "application/json"})
    return f"Status: {r.status_code}"

@mcp.tool()
def reload_flows() -> str:
    """Reload node-red flows from disk. Always run this after update_flows"""
    r = requests.post(f"{NODE_RED_URL}/flows")
    return f"Status: {r.status_code}"

mcp.run(transport="streamable-http", host="0.0.0.0", port=8121)