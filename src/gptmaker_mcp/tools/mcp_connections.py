"""GPTMaker tools — MCP Connections and Tools."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def add_mcp_to_agent(
    agent_id: str,
    name: str,
    description: str,
    mcp_url: str,
    url_type: str,
    auth_type: str,
    headers: Optional[dict] = None,
) -> str:
    """Add an MCP (Model Context Protocol) server connection to an agent.

    POST /v2/agent/{agentId}/mcp/add

    Args:
        agent_id: Agent ID.
        name: Display name for this MCP connection.
        description: Description of what this MCP server provides.
        mcp_url: URL of the MCP server endpoint.
        url_type: Connection type. Values: SSE, STREAMABLEHTTP.
        auth_type: Authentication type. Values: NO_OAUTH, OAUTH, HEADERS.
        headers: Dictionary of HTTP headers for authentication (used with HEADERS auth_type).
    """
    body = {
        "name": name,
        "description": description,
        "mcpUrl": mcp_url,
        "urlType": url_type,
        "authType": auth_type,
        "headers": headers,
    }
    result = await _client.post(f"/v2/agent/{agent_id}/mcp/add", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def connect_mcp(code: str, state: str) -> str:
    """Complete an OAuth MCP connection flow.

    POST /v2/mcp/connect

    Args:
        code: OAuth authorization code.
        state: OAuth state parameter.
    """
    result = await _client.post("/v2/mcp/connect", json={"code": code, "state": state})
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_mcp(mcp_id: str) -> str:
    """Delete an MCP connection from an agent.

    DELETE /v2/mcp/{mcpId}

    Args:
        mcp_id: MCP connection ID.
    """
    result = await _client.delete(f"/v2/mcp/{mcp_id}")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def list_mcp_tools(mcp_id: str) -> str:
    """List all tools available in an MCP connection.

    GET /v2/mcp/{mcpId}/tools

    Args:
        mcp_id: MCP connection ID.
    """
    result = await _client.get(f"/v2/mcp/{mcp_id}/tools")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def activate_mcp_tool(mcp_id: str, tool_id: str) -> str:
    """Activate a specific tool within an MCP connection.

    GET /v2/mcp/{mcpId}/tool/{toolId}/active

    Args:
        mcp_id: MCP connection ID.
        tool_id: Tool ID to activate.
    """
    result = await _client.get(f"/v2/mcp/{mcp_id}/tool/{tool_id}/active")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def deactivate_mcp_tool(mcp_id: str, tool_id: str) -> str:
    """Deactivate a specific tool within an MCP connection.

    GET /v2/mcp/{mcpId}/tool/{toolId}/inactive

    Args:
        mcp_id: MCP connection ID.
        tool_id: Tool ID to deactivate.
    """
    result = await _client.get(f"/v2/mcp/{mcp_id}/tool/{tool_id}/inactive")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def sync_mcp_tools(mcp_id: str) -> str:
    """Synchronize the tool list from the remote MCP server.

    GET /v2/mcp/{mcpId}/sync-tools

    Args:
        mcp_id: MCP connection ID.
    """
    result = await _client.get(f"/v2/mcp/{mcp_id}/sync-tools")
    return json.dumps(result, indent=2, ensure_ascii=False)
