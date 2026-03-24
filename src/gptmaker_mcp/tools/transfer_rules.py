"""GPTMaker tools — Transfer Rules."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def list_transfer_rules(agent_id: str) -> str:
    """List all transfer rules for an agent.
    Transfer rules define conditions for transferring conversations to humans or other agents.

    GET /v2/agent/{id}/transfer-rules

    Args:
        agent_id: Agent ID.
    """
    result = await _client.get(f"/v2/agent/{agent_id}/transfer-rules")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def create_transfer_rule(
    agent_id: str,
    type_: Optional[str] = None,
    instructions: Optional[str] = None,
    return_on_finish: Optional[bool] = None,
    user_id: Optional[str] = None,
    destination_agent_id: Optional[str] = None,
) -> str:
    """Create a transfer rule for an agent.

    POST /v2/agent/{agentId}/transfer-rules

    Args:
        agent_id: Agent ID.
        type_: Transfer destination type. Values: HUMAN, AGENT.
        instructions: Conditions or instructions for when to trigger this transfer.
        return_on_finish: Return conversation to original agent when transfer finishes.
        user_id: Human user ID to transfer to (for HUMAN type).
        destination_agent_id: Destination agent ID to transfer to (for AGENT type).
    """
    body = {
        "type": type_,
        "instructions": instructions,
        "returnOnFinish": return_on_finish,
        "userId": user_id,
        "agentId": destination_agent_id,
    }
    result = await _client.post(f"/v2/agent/{agent_id}/transfer-rules", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_transfer_rule(
    agent_id: str,
    transfer_rule_id: str,
    type_: Optional[str] = None,
    instructions: Optional[str] = None,
    return_on_finish: Optional[bool] = None,
    user_id: Optional[str] = None,
    destination_agent_id: Optional[str] = None,
) -> str:
    """Update an existing transfer rule.

    PUT /v2/agent/{agentId}/transfer-rules/{transfer-rule-id}

    Args:
        agent_id: Agent ID.
        transfer_rule_id: Transfer rule ID.
        type_: Transfer destination type. Values: HUMAN, AGENT.
        instructions: Conditions or instructions for when to trigger this transfer.
        return_on_finish: Return conversation to original agent when transfer finishes.
        user_id: Human user ID to transfer to (for HUMAN type).
        destination_agent_id: Destination agent ID to transfer to (for AGENT type).
    """
    body = {
        "type": type_,
        "instructions": instructions,
        "returnOnFinish": return_on_finish,
        "userId": user_id,
        "agentId": destination_agent_id,
    }
    result = await _client.put(
        f"/v2/agent/{agent_id}/transfer-rules/{transfer_rule_id}",
        json=body,
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_transfer_rule(agent_id: str, transfer_rule_id: str) -> str:
    """Delete a transfer rule.

    DELETE /v2/agent/{agentId}/transfer-rules/{transfer-rule-id}

    Args:
        agent_id: Agent ID.
        transfer_rule_id: Transfer rule ID.
    """
    result = await _client.delete(
        f"/v2/agent/{agent_id}/transfer-rules/{transfer_rule_id}"
    )
    return json.dumps(result, indent=2, ensure_ascii=False)
