"""GPTMaker tools — Agents."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def list_agents(
    workspace_id: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    query: Optional[str] = None,
) -> str:
    """List all agents in a workspace.

    GET /v2/workspace/{workspaceId}/agents

    Args:
        workspace_id: Workspace ID.
        page: Page number for pagination.
        page_size: Number of items per page.
        query: Search query to filter agents by name.
    """
    result = await _client.get(
        f"/v2/workspace/{workspace_id}/agents",
        params={"page": page, "pageSize": page_size, "query": query},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def create_agent(
    workspace_id: str,
    name: Optional[str] = None,
    avatar: Optional[str] = None,
    behavior: Optional[str] = None,
    communication_type: Optional[str] = None,
    type_: Optional[str] = None,
    job_name: Optional[str] = None,
    job_site: Optional[str] = None,
    job_description: Optional[str] = None,
) -> str:
    """Create a new agent in a workspace.

    POST /v2/workspace/{workspaceId}/agents

    Args:
        workspace_id: Workspace ID.
        name: Agent name.
        avatar: URL of the agent avatar image.
        behavior: Agent behavior/personality description.
        communication_type: Communication style. Values: FORMAL, NORMAL, RELAXED.
        type_: Agent objective. Values: SUPPORT, SALE, PERSONAL.
        job_name: Company or product name the agent will work for.
        job_site: Company website URL.
        job_description: Company description.
    """
    body = {
        "name": name,
        "avatar": avatar,
        "behavior": behavior,
        "communicationType": communication_type,
        "type": type_,
        "jobName": job_name,
        "jobSite": job_site,
        "jobDescription": job_description,
    }
    result = await _client.post(f"/v2/workspace/{workspace_id}/agents", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def get_agent(agent_id: str) -> str:
    """Get an agent by ID.

    GET /v2/agent/{agentId}

    Args:
        agent_id: Agent ID.
    """
    result = await _client.get(f"/v2/agent/{agent_id}")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_agent(
    agent_id: str,
    name: Optional[str] = None,
    avatar: Optional[str] = None,
    behavior: Optional[str] = None,
    communication_type: Optional[str] = None,
    type_: Optional[str] = None,
    job_name: Optional[str] = None,
    job_site: Optional[str] = None,
    job_description: Optional[str] = None,
) -> str:
    """Update an agent's details.

    PUT /v2/agent/{agentId}

    Args:
        agent_id: Agent ID.
        name: Agent name.
        avatar: URL of the agent avatar image.
        behavior: Agent behavior/personality description.
        communication_type: Communication style. Values: FORMAL, NORMAL, RELAXED.
        type_: Agent objective. Values: SUPPORT, SALE, PERSONAL.
        job_name: Company or product name the agent will work for.
        job_site: Company website URL.
        job_description: Company description.
    """
    body = {
        "name": name,
        "avatar": avatar,
        "behavior": behavior,
        "communicationType": communication_type,
        "type": type_,
        "jobName": job_name,
        "jobSite": job_site,
        "jobDescription": job_description,
    }
    result = await _client.put(f"/v2/agent/{agent_id}", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_agent(agent_id: str) -> str:
    """Delete an agent.

    DELETE /v2/agent/{agentId}

    Args:
        agent_id: Agent ID.
    """
    result = await _client.delete(f"/v2/agent/{agent_id}")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def activate_agent(agent_id: str) -> str:
    """Activate an agent (enable it to receive messages).

    PUT /v2/agent/{agentId}/active

    Args:
        agent_id: Agent ID.
    """
    result = await _client.put(f"/v2/agent/{agent_id}/active")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def deactivate_agent(agent_id: str) -> str:
    """Deactivate an agent (stop it from receiving messages).

    PUT /v2/agent/{agentId}/inactive

    Args:
        agent_id: Agent ID.
    """
    result = await _client.put(f"/v2/agent/{agent_id}/inactive")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def get_agent_settings(agent_id: str) -> str:
    """Get an agent's configuration settings.

    GET /v2/agent/{agentId}/settings

    Args:
        agent_id: Agent ID.
    """
    result = await _client.get(f"/v2/agent/{agent_id}/settings")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_agent_settings(
    agent_id: str,
    prefer_model: Optional[str] = None,
    timezone: Optional[str] = None,
    enabled_human_transfer: Optional[bool] = None,
    enabled_reminder: Optional[bool] = None,
    split_messages: Optional[bool] = None,
    enabled_emoji: Optional[bool] = None,
    limit_subjects: Optional[bool] = None,
    message_grouping_time: Optional[str] = None,
    sign_messages: Optional[bool] = None,
    max_daily_messages: Optional[int] = None,
    max_daily_messages_limit_action: Optional[str] = None,
    knowledge_by_function: Optional[bool] = None,
    on_lack_knowledge: Optional[str] = None,
) -> str:
    """Update an agent's configuration settings.

    PUT /v2/agent/{agentId}/settings

    Args:
        agent_id: Agent ID.
        prefer_model: AI model to use. Values: GPT_5, GPT_5_MINI, GPT_5_1, GPT_5_2,
            GPT_5_MINI_V2, GPT_4_TURBO, OPEN_AI_04, OPEN_AI_03_MINI_BETA, GPT_4_1,
            GPT_4_1_MINI, GPT_4_O_MINI, GPT_4_O, OPEN_AI_O3_MINI, OPEN_AI_O4_MINI,
            OPEN_AI_O3, OPEN_AI_O1, GPT_4, CLAUDE_4_5_SONNET, CLAUDE_3_5_SONNET,
            CLAUDE_3_7_SONNET, CLAUDE_3_5_HAIKU, DEEPINFRA_LLAMA3_3, QWEN_2_5_MAX,
            DEEPSEEK_CHAT, SABIA_3, SABIA_3_1.
        timezone: Timezone string (e.g. America/Sao_Paulo).
        enabled_human_transfer: Allow transferring conversation to a human agent.
        enabled_reminder: Enable reminder messages.
        split_messages: Split long responses into multiple messages.
        enabled_emoji: Allow emojis in responses.
        limit_subjects: Restrict agent to specific topics.
        message_grouping_time: Time to group messages before processing.
            Values: NO_GROUP, FIVE_SEC, TEN_SEC, THIRD_SEC, ONE_MINUTE.
        sign_messages: Sign messages with agent name.
        max_daily_messages: Maximum messages the agent can send per day.
        max_daily_messages_limit_action: Action when daily limit is reached.
            Values: TEMP_BLOCK_30S, TEMP_BLOCK_5M, TEMP_BLOCK_10M, TEMP_BLOCK_30M,
            TEMP_BLOCK_1H, BLOCK, TRANSFER.
        knowledge_by_function: Use function calling for knowledge retrieval.
        on_lack_knowledge: Response when agent lacks knowledge.
    """
    body = {
        "prefferModel": prefer_model,
        "timezone": timezone,
        "enabledHumanTransfer": enabled_human_transfer,
        "enabledReminder": enabled_reminder,
        "splitMessages": split_messages,
        "enabledEmoji": enabled_emoji,
        "limitSubjects": limit_subjects,
        "messageGroupingTime": message_grouping_time,
        "signMessages": sign_messages,
        "maxDailyMessages": max_daily_messages,
        "maxDailyMessagesLimitAction": max_daily_messages_limit_action,
        "knowledgeByFunction": knowledge_by_function,
        "onLackKnowLedge": on_lack_knowledge,
    }
    result = await _client.put(f"/v2/agent/{agent_id}/settings", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def get_agent_webhooks(agent_id: str) -> str:
    """Get the configured webhooks for an agent.

    GET /v2/agent/{agentId}/webhooks

    Args:
        agent_id: Agent ID.
    """
    result = await _client.get(f"/v2/agent/{agent_id}/webhooks")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_agent_webhooks(
    agent_id: str,
    on_new_message: Optional[str] = None,
    on_lack_knowledge: Optional[str] = None,
    on_transfer: Optional[str] = None,
    on_first_interaction: Optional[str] = None,
    on_start_interaction: Optional[str] = None,
    on_finish_interaction: Optional[str] = None,
    on_create_event: Optional[str] = None,
    on_cancel_event: Optional[str] = None,
) -> str:
    """Update the webhook URLs for agent events.

    PUT /v2/agent/{agentId}/webhooks

    Args:
        agent_id: Agent ID.
        on_new_message: Webhook URL called when a new message arrives.
        on_lack_knowledge: Webhook URL called when agent lacks knowledge.
        on_transfer: Webhook URL called when conversation is transferred.
        on_first_interaction: Webhook URL called on first contact interaction.
        on_start_interaction: Webhook URL called when interaction starts.
        on_finish_interaction: Webhook URL called when interaction finishes.
        on_create_event: Webhook URL called when a calendar event is created.
        on_cancel_event: Webhook URL called when a calendar event is cancelled.
    """
    body = {
        "onNewMessage": on_new_message,
        "onLackKnowLedge": on_lack_knowledge,
        "onTransfer": on_transfer,
        "onFirstInteraction": on_first_interaction,
        "onStartInteraction": on_start_interaction,
        "onFinishInteraction": on_finish_interaction,
        "onCreateEvent": on_create_event,
        "onCancelEvent": on_cancel_event,
    }
    result = await _client.put(f"/v2/agent/{agent_id}/webhooks", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def get_agent_credits_spent(
    agent_id: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
) -> str:
    """Get credit consumption for an agent, optionally filtered by date.

    GET /v2/agent/{agentId}/credits-spent

    Args:
        agent_id: Agent ID.
        year: Filter by year (e.g. 2025).
        month: Filter by month (1-12).
        day: Filter by day (1-31).
    """
    result = await _client.get(
        f"/v2/agent/{agent_id}/credits-spent",
        params={"year": year, "month": month, "day": day},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def list_agent_behavior_history(
    agent_id: str,
    page: int,
    page_size: int,
) -> str:
    """List the behavior history log for an agent.

    GET /v2/agent/{id}/list-behavior-history

    Args:
        agent_id: Agent ID.
        page: Page number (required).
        page_size: Number of items per page (required).
    """
    result = await _client.get(
        f"/v2/agent/{agent_id}/list-behavior-history",
        params={"page": page, "pageSize": page_size},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def chat_with_agent(
    agent_id: str,
    context_id: str,
    prompt: Optional[str] = None,
    image: Optional[str] = None,
    audio: Optional[str] = None,
    callback_url: Optional[str] = None,
    on_finish_callback: Optional[str] = None,
    chat_name: Optional[str] = None,
    chat_picture: Optional[str] = None,
    phone: Optional[str] = None,
) -> str:
    """Send a message to an agent and get a response. Supports text, image, or audio.

    POST /v2/agent/{agentId}/conversation

    Args:
        agent_id: Agent ID.
        context_id: External identifier for the client/session (e.g. user ID or phone).
        prompt: Text message to send to the agent (for text or text+image).
        image: Image URL to send alongside a text prompt.
        audio: Audio file URL to send (use instead of prompt for voice messages).
        callback_url: Webhook URL to receive the async response.
        on_finish_callback: Webhook URL called when the agent finishes responding.
        chat_name: Display name for the chat contact.
        chat_picture: Profile picture URL for the chat contact.
        phone: WhatsApp phone number of the contact.
    """
    body: dict = {"contextId": context_id}
    if audio:
        body["audio"] = audio
    else:
        if prompt:
            body["prompt"] = prompt
        if image:
            body["image"] = image
    if callback_url:
        body["callbackUrl"] = callback_url
    if on_finish_callback:
        body["onFinishCallback"] = on_finish_callback
    if chat_name:
        body["chatName"] = chat_name
    if chat_picture:
        body["chatPicture"] = chat_picture
    if phone:
        body["phone"] = phone

    result = await _client.post(f"/v2/agent/{agent_id}/conversation", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def add_agent_context(
    agent_id: str,
    context_id: str,
    role: str,
    prompt: Optional[str] = None,
    image: Optional[str] = None,
    audio: Optional[str] = None,
) -> str:
    """Add a message to an agent's conversation context without triggering a response.

    POST /v2/agent/{agentId}/add-message

    Args:
        agent_id: Agent ID.
        context_id: External identifier for the client/session.
        role: Message role. Values: user, assistant.
        prompt: Text content of the message.
        image: Image URL to add to the context.
        audio: Audio file URL to add to the context.
    """
    body: dict = {"contextId": context_id, "role": role}
    if audio:
        body["audio"] = audio
    else:
        if prompt:
            body["prompt"] = prompt
        if image:
            body["image"] = image

    result = await _client.post(f"/v2/agent/{agent_id}/add-message", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)
