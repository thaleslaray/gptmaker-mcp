"""GPTMaker tools — Interactions and Export."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def list_interactions(
    workspace_id: str,
    agent_id: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
) -> str:
    """List all interactions (completed conversations) in a workspace.

    GET /v2/workspace/{workspaceId}/interactions

    Args:
        workspace_id: Workspace ID.
        agent_id: Filter interactions by agent ID.
        page: Page number for pagination.
        page_size: Number of items per page.
    """
    result = await _client.get(
        f"/v2/workspace/{workspace_id}/interactions",
        params={"agentId": agent_id, "page": page, "pageSize": page_size},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def get_interaction_messages(interaction_id: str) -> str:
    """Get all messages from a specific interaction.

    GET /v2/interaction/{interactionId}/messages

    Args:
        interaction_id: Interaction ID.
    """
    result = await _client.get(f"/v2/interaction/{interaction_id}/messages")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_interaction(interaction_id: str) -> str:
    """Delete an interaction and its messages.

    DELETE /v2/interaction/{id}

    Args:
        interaction_id: Interaction ID.
    """
    result = await _client.delete(f"/v2/interaction/{interaction_id}")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def export_interactions(
    workspace_id: str,
    page: Optional[int] = None,
    pagesize: Optional[int] = None,
) -> str:
    """Export interactions/attendances as CSV data.
    Returns contactName, channelType, status, agentName, startAt, resolvedAt, duration, protocol.
    Pass no pagination params to export all interactions.

    POST /v2/workspace/{workspaceId}/export

    Args:
        workspace_id: Workspace ID.
        page: Page number (omit to export all).
        pagesize: Number of items per page (omit to export all).
    """
    body: dict = {}
    if page is not None:
        body["page"] = page
    if pagesize is not None:
        body["pagesize"] = pagesize

    result = await _client.post(f"/v2/workspace/{workspace_id}/export", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)
