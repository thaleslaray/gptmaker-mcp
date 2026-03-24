"""GPTMaker tools — Intentions."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def list_intentions(
    agent_id: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    query: Optional[str] = None,
) -> str:
    """List all intentions (webhook triggers) for an agent.

    GET /v2/agent/{agentId}/intentions

    Args:
        agent_id: Agent ID.
        page: Page number for pagination.
        page_size: Number of items per page.
        query: Search query to filter intentions.
    """
    result = await _client.get(
        f"/v2/agent/{agent_id}/intentions",
        params={"page": page, "pageSize": page_size, "query": query},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def create_intention(
    agent_id: str,
    description: str,
    type_: str,
    http_method: str,
    url: str,
    auto_generate_params: bool,
    auto_generate_body: bool,
    details: Optional[str] = None,
    instructions: Optional[str] = None,
    fields: Optional[list] = None,
    headers: Optional[list] = None,
    params: Optional[list] = None,
    variables: Optional[list] = None,
    request_body: Optional[str] = None,
) -> str:
    """Create a new intention (external webhook trigger) for an agent.

    POST /v2/agent/{agentId}/intentions

    Args:
        agent_id: Agent ID.
        description: What this intention does (shown to the AI agent).
        type_: Intention type. Values: WEBHOOK, INSTRUCTIONS.
        http_method: HTTP method for the webhook. Values: GET, POST.
        url: Webhook URL to call when this intention is triggered.
        auto_generate_params: Let AI automatically generate query parameters.
        auto_generate_body: Let AI automatically generate the request body.
        details: Additional details about when to trigger this intention.
        instructions: Instructions for the agent on how to use this intention.
        fields: List of fields to extract from the conversation.
        headers: List of HTTP headers [{key, value}] to include in the webhook call.
        params: List of query parameters [{key, value}] for the webhook.
        variables: List of variables to pass to the webhook.
        request_body: JSON body template for POST requests.
    """
    body = {
        "description": description,
        "type": type_,
        "httpMethod": http_method,
        "url": url,
        "autoGenerateParams": auto_generate_params,
        "autoGenerateBody": auto_generate_body,
        "details": details,
        "instructions": instructions,
        "fields": fields,
        "headers": headers,
        "params": params,
        "variables": variables,
        "requestBody": request_body,
    }
    result = await _client.post(f"/v2/agent/{agent_id}/intentions", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_intention(
    intention_id: str,
    description: Optional[str] = None,
    type_: Optional[str] = None,
    http_method: Optional[str] = None,
    url: Optional[str] = None,
    auto_generate_params: Optional[bool] = None,
    auto_generate_body: Optional[bool] = None,
    details: Optional[str] = None,
    instructions: Optional[str] = None,
    fields: Optional[list] = None,
    headers: Optional[list] = None,
    params: Optional[list] = None,
    variables: Optional[list] = None,
    request_body: Optional[str] = None,
) -> str:
    """Update an existing intention.

    PUT /v2/intention/{intentionId}

    Args:
        intention_id: Intention ID.
        description: What this intention does.
        type_: Intention type. Values: WEBHOOK, INSTRUCTIONS.
        http_method: HTTP method. Values: GET, POST.
        url: Webhook URL.
        auto_generate_params: Let AI generate query parameters automatically.
        auto_generate_body: Let AI generate the request body automatically.
        details: Additional details.
        instructions: Agent instructions for using this intention.
        fields: Fields to extract from conversation.
        headers: HTTP headers [{key, value}].
        params: Query parameters [{key, value}].
        variables: Variables to pass.
        request_body: JSON body template.
    """
    body = {
        "description": description,
        "type": type_,
        "httpMethod": http_method,
        "url": url,
        "autoGenerateParams": auto_generate_params,
        "autoGenerateBody": auto_generate_body,
        "details": details,
        "instructions": instructions,
        "fields": fields,
        "headers": headers,
        "params": params,
        "variables": variables,
        "requestBody": request_body,
    }
    result = await _client.put(f"/v2/intention/{intention_id}", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_intention(intention_id: str) -> str:
    """Delete an intention.

    DELETE /v2/intention/{intentionId}

    Args:
        intention_id: Intention ID.
    """
    result = await _client.delete(f"/v2/intention/{intention_id}")
    return json.dumps(result, indent=2, ensure_ascii=False)
