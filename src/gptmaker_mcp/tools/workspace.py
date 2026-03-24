"""GPTMaker tools — Workspace."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def list_workspaces() -> str:
    """List all workspaces for the authenticated account.

    GET /v2/workspaces
    """
    result = await _client.get("/v2/workspaces")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def get_workspace_credits(workspace_id: str) -> str:
    """Get available credit balance for a workspace.

    GET /v2/workspace/{workspaceId}/credits

    Args:
        workspace_id: Workspace ID.
    """
    result = await _client.get(f"/v2/workspace/{workspace_id}/credits")
    return json.dumps(result, indent=2, ensure_ascii=False)
