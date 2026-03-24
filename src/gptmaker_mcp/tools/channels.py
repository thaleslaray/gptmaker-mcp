"""GPTMaker tools — Channels."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()

CHANNEL_TYPES = "Z_API, WHATSAPP, INSTAGRAM, CLOUD_API, TELEGRAM, WIDGET, MESSENGER, MERCADO_LIVRE, TWILIO_SMS"


async def list_agent_channels(
    agent_id: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    query: Optional[str] = None,
) -> str:
    """List all channels linked to an agent.

    GET /v2/agent/{agentId}/search

    Args:
        agent_id: Agent ID.
        page: Page number for pagination.
        page_size: Number of items per page.
        query: Search query to filter channels by name.
    """
    result = await _client.get(
        f"/v2/agent/{agent_id}/search",
        params={"page": page, "pageSize": page_size, "query": query},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def list_workspace_channels(
    workspace_id: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    query: Optional[str] = None,
    agent_id: Optional[str] = None,
) -> str:
    """List all channels in a workspace.

    GET /v2/workspace/{workspaceId}/channels

    Args:
        workspace_id: Workspace ID.
        page: Page number for pagination.
        page_size: Number of items per page.
        query: Search query to filter channels by name.
        agent_id: Filter channels by linked agent ID.
    """
    result = await _client.get(
        f"/v2/workspace/{workspace_id}/channels",
        params={"page": page, "pageSize": page_size, "query": query, "agentId": agent_id},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def create_agent_channel(
    agent_id: str,
    name: str,
    type_: str,
) -> str:
    """Create a new channel linked to an agent.

    POST /v2/agent/{agentId}/create-channel

    Args:
        agent_id: Agent ID to link the channel to.
        name: Channel name.
        type_: Channel type. Values: WHATSAPP, INSTAGRAM, CLOUD_API, TELEGRAM,
            WIDGET, MESSENGER, MERCADO_LIVRE.
    """
    result = await _client.post(
        f"/v2/agent/{agent_id}/create-channel",
        json={"name": name, "type": type_},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def create_workspace_channel(
    workspace_id: str,
    name: str,
    type_: Optional[str] = None,
) -> str:
    """Create a new channel in a workspace (not linked to a specific agent).

    POST /v2/workspace/{workspaceId}/create-channel

    Args:
        workspace_id: Workspace ID.
        name: Channel name.
        type_: Channel type. Values: Z_API, WHATSAPP, INSTAGRAM, CLOUD_API,
            TELEGRAM, WIDGET, MESSENGER, MERCADO_LIVRE, TWILIO_SMS.
    """
    result = await _client.post(
        f"/v2/workspace/{workspace_id}/create-channel",
        json={"name": name, "type": type_},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def create_channel_for_assistant(
    assistant_id: str,
    type_: str,
    name: str,
    linked_assistant_id: Optional[str] = None,
) -> str:
    """Create a channel with type in the path (most up-to-date channel creation endpoint).

    POST /v2/assistant/{assistantId}/create-channel/{type}

    Args:
        assistant_id: Agent/assistant ID that owns this channel.
        type_: Channel type in path. Values: Z_API, WHATSAPP, INSTAGRAM, CLOUD_API,
            TELEGRAM, WIDGET, MESSENGER, MERCADO_LIVRE, TWILIO_SMS.
        name: Channel name (required).
        linked_assistant_id: Optional agent ID to link to the channel. If not provided,
            channel is created without an agent.
    """
    body: dict = {"name": name}
    if linked_assistant_id:
        body["assistantId"] = linked_assistant_id

    result = await _client.post(
        f"/v2/assistant/{assistant_id}/create-channel/{type_}",
        json=body,
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_channel(
    channel_id: str,
    name: str,
    agent_id: Optional[str] = None,
) -> str:
    """Update a channel's name and/or linked agent.

    PUT /v2/channel/{channelId}

    Args:
        channel_id: Channel ID.
        name: New channel name (required).
        agent_id: Agent ID to link to this channel (optional).
    """
    result = await _client.put(
        f"/v2/channel/{channel_id}",
        json={"name": name, "agentId": agent_id},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_channel(channel_id: str) -> str:
    """Delete a channel.

    DELETE /v2/channel/{channelId}

    Args:
        channel_id: Channel ID.
    """
    result = await _client.delete(f"/v2/channel/{channel_id}")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def get_channel_qr_code(channel_id: str) -> str:
    """Get the WhatsApp QR code for a channel (used for WhatsApp Web connection).

    GET /v2/channel/{channelId}/qr-code

    Args:
        channel_id: Channel ID.
    """
    result = await _client.get(f"/v2/channel/{channel_id}/qr-code")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def get_channel_config(channel_id: str) -> str:
    """Get the configuration for a channel.

    GET /v2/channel/{channelId}/config

    Args:
        channel_id: Channel ID.
    """
    result = await _client.get(f"/v2/channel/{channel_id}/config")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_channel_config(
    channel_id: str,
    audio_action: Optional[str] = None,
    start_trigger: Optional[str] = None,
    end_trigger: Optional[str] = None,
) -> str:
    """Update a channel's configuration settings.

    PUT /v2/channel/{id}/config

    Args:
        channel_id: Channel ID.
        audio_action: Action to perform for audio messages.
        start_trigger: Keyword/phrase to start the agent conversation.
        end_trigger: Keyword/phrase to end the agent conversation.
    """
    body = {
        "audioAction": audio_action,
        "startTrigger": start_trigger,
        "endTrigger": end_trigger,
    }
    result = await _client.put(f"/v2/channel/{channel_id}/config", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def get_channel_widget_links(channel_id: str) -> str:
    """Get the embed script links for a widget channel.

    GET /v2/channel/{channelId}/widget-links

    Args:
        channel_id: Channel ID (must be a WIDGET type channel).
    """
    result = await _client.get(f"/v2/channel/{channel_id}/widget-links")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_channel_widget_settings(
    channel_id: str,
    is_public: Optional[bool] = None,
    initial_message: Optional[str] = None,
    origins: Optional[list] = None,
    suggest_messages: Optional[list] = None,
    header_background: Optional[str] = None,
    header_color: Optional[str] = None,
    message_user_background: Optional[str] = None,
    button_background: Optional[str] = None,
) -> str:
    """Update the visual settings for a widget channel.

    PUT /v2/channel/{channelId}/widget-settings

    Args:
        channel_id: Channel ID (must be a WIDGET type channel).
        is_public: Whether the widget is publicly accessible.
        initial_message: Initial greeting message shown in the widget.
        origins: List of allowed origins (domains) for the widget.
        suggest_messages: List of suggested quick-reply messages for users.
        header_background: Header background color (hex, e.g. #4A90E2).
        header_color: Header text/icon color (hex).
        message_user_background: User message bubble background color (hex).
        button_background: Send button background color (hex).
    """
    body = {
        "isPublic": is_public,
        "initialMessage": initial_message,
        "origins": origins,
        "suggestMessages": suggest_messages,
        "headerBackground": header_background,
        "headerColor": header_color,
        "messageUserBackground": message_user_background,
        "buttonBackground": button_background,
    }
    result = await _client.put(f"/v2/channel/{channel_id}/widget-settings", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def start_channel_conversation(
    channel_id: str,
    phone: str,
    message: Optional[str] = None,
    image: Optional[str] = None,
    video: Optional[str] = None,
    audio: Optional[str] = None,
    document: Optional[str] = None,
    document_name: Optional[str] = None,
    document_mimetype: Optional[str] = None,
) -> str:
    """Start a new outbound conversation via a channel. Supports text, image, video, audio, or document.

    POST /v2/channel/{channelId}/start-conversation

    Args:
        channel_id: Channel ID.
        phone: Recipient's phone number (required).
        message: Text message to send.
        image: Image URL to send.
        video: Video URL to send.
        audio: Audio URL to send.
        document: Document URL to send.
        document_name: Document filename.
        document_mimetype: Document MIME type (e.g. application/pdf).
    """
    body: dict = {"phone": phone}
    if image:
        body["image"] = image
    elif video:
        body["video"] = video
    elif audio:
        body["audio"] = audio
    elif document:
        body["document"] = document
        if document_name:
            body["documentName"] = document_name
        if document_mimetype:
            body["documentMimetype"] = document_mimetype
    else:
        if message:
            body["message"] = message

    result = await _client.post(f"/v2/channel/{channel_id}/start-conversation", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)
