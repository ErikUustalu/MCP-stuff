from fastmcp import FastMCP
import requests
import json
import os

mcp = FastMCP("mcp-server")

# Node Red
NODE_RED_URL = os.environ.get("NODE_RED_URL")

nodered = FastMCP("nodered")

@nodered.tool()
def nodered_get_flows():
    """Get all node-red flows as json"""
    return requests.get(f"{NODE_RED_URL}/flows").text

@nodered.tool()
def nodered_update_flows(flows: str) -> str:
    """Replace all node-red flows with provided json"""
    r = requests.post(f"{NODE_RED_URL}/flows", data=flows, headers={"Content-Type": "application/json"})
    return f"Status: {r.status_code}"

@nodered.tool()
def nodered_reload_flows() -> str:
    """Reload node-red flows from disk. Always run this after update_flows"""
    r = requests.post(f"{NODE_RED_URL}/flows")
    return f"Status: {r.status_code}"

# Ntfy

NTFY_URL = os.environ.get("NTFY_URL")

ntfy = FastMCP("ntfy")

@ntfy.tool()
def ntfy_send_notification(title: str, message: str) -> str:
    """Send ntfy notification"""
    r = requests.post(NTFY_URL, data=message, headers={"Title": title})
    return f"Status: {r.status_code}"

mcp.mount(nodered)
mcp.mount(ntfy)

mcp.run(transport="streamable-http", host="0.0.0.0", port=8121)