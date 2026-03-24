"""GPTMaker tools — Idle Actions."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def list_idle_actions(agent_id: str) -> str:
    """List all idle actions configured for an agent.
    Idle actions are triggered when a contact has no activity for a set period.

    GET /v2/agent/{agentId}/idle-actions

    Args:
        agent_id: Agent ID.
    """
    result = await _client.get(f"/v2/agent/{agent_id}/idle-actions")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def create_idle_actions(
    agent_id: str,
    actions: Optional[list] = None,
    finish_on: Optional[dict] = None,
) -> str:
    """Create idle actions for an agent.

    POST /v2/agent/{agentId}/idle-actions

    Args:
        agent_id: Agent ID.
        actions: List of action objects defining what to do when idle.
            Each action typically has: {type, delay, message} or similar structure.
        finish_on: Condition that ends the idle action sequence.
    """
    body = {"actions": actions, "finishOn": finish_on}
    result = await _client.post(f"/v2/agent/{agent_id}/idle-actions", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_idle_actions(
    agent_id: str,
    actions: Optional[list] = None,
    finish_on: Optional[dict] = None,
) -> str:
    """Update the idle actions for an agent.

    PUT /v2/agent/{agentId}/idle-actions

    Args:
        agent_id: Agent ID.
        actions: Updated list of action objects.
        finish_on: Updated condition that ends the idle action sequence.
    """
    body = {"actions": actions, "finishOn": finish_on}
    result = await _client.put(f"/v2/agent/{agent_id}/idle-actions", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_idle_actions(agent_id: str) -> str:
    """Delete all idle actions for an agent.

    DELETE /v2/agent/{agentId}/idle-actions

    Args:
        agent_id: Agent ID.
    """
    result = await _client.delete(f"/v2/agent/{agent_id}/idle-actions")
    return json.dumps(result, indent=2, ensure_ascii=False)
