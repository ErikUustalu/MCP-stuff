from fastmcp import FastMCP
import requests
import json
import os
import paramiko

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
def nodered_reload_flows():
    """Reload node-red flows from disk. Always run this after update_flows"""
    r = requests.post(
        f"{NODE_RED_URL}/flows",
        headers={"Node-RED-Deployment-Type": "reload"}
    )
    return r.text

# Ntfy

NTFY_URL = os.environ.get("NTFY_URL")

ntfy = FastMCP("ntfy")

@ntfy.tool()
def ntfy_send_notification(title: str, message: str) -> str:
    """Send ntfy notification"""
    r = requests.post(NTFY_URL, data=message, headers={"Title": title})
    return f"Status: {r.status_code}"

# Glances

GLANCES_URL = os.environ.get("GLANCES_URL")

glances = FastMCP("glances")

@glances.tool()
def glances_get_stats_quick() -> str:
    """Get a quick overview of beelink's stats"""
    return requests.get(f"{GLANCES_URL}/api/4/quicklook").text

@glances.tool()
def glances_get_sensors() -> str:
    """Get beelink's temp sensors data"""
    return requests.get(f"{GLANCES_URL}/api/4/sensors").text

@glances.tool()
def glances_get_processes() -> str:
    """Get beelink's processes data"""
    return requests.get(f"{GLANCES_URL}/api/4/processlist").text

@glances.tool()
def glances_get_containers() -> str:
    """Get beelink's docker containers data"""
    return requests.get(f"{GLANCES_URL}/api/4/containers").text

# SSH

SSH_HOST = os.environ.get("SSH_HOST")
SSH_USER = os.environ.get("SSH_USER")
SSH_PASSWORD = os.environ.get("SSH_PASSWORD")

ssh = FastMCP("ssh")

@ssh.tool()
def ssh_run_command(command: str, timeout: int) -> str:
    """Run a command on beelink and return the output"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD, timeout=timeout)
        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        return stdout.read().decode() + stderr.read().decode()
    except paramiko.SSHException as e:
        return f"SSH error: {str(e)}"
    finally:
        client.close()

mcp.mount(nodered)
mcp.mount(ntfy)
mcp.mount(glances)
mcp.mount(ssh)

mcp.run(transport="streamable-http", host="0.0.0.0", port=8121, host_origin_protection=False)