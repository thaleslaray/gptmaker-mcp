"""GPTMaker tools — Chats and Messages."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def list_chats(
    workspace_id: str,
    agent_id: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    query: Optional[str] = None,
) -> str:
    """List all chats in a workspace.

    GET /v2/workspace/{workspaceId}/chats

    Args:
        workspace_id: Workspace ID.
        agent_id: Filter chats by agent ID.
        page: Page number for pagination.
        page_size: Number of items per page.
        query: Search query to filter chats by contact name.
    """
    result = await _client.get(
        f"/v2/workspace/{workspace_id}/chats",
        params={"agentId": agent_id, "page": page, "pageSize": page_size, "query": query},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_chat(chat_id: str) -> str:
    """Delete a chat and all its messages.

    DELETE /v2/chat/{chatId}

    Args:
        chat_id: Chat ID.
    """
    result = await _client.delete(f"/v2/chat/{chat_id}")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def list_chat_messages(
    chat_id: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
) -> str:
    """List all messages in a chat.

    GET /v2/chat/{chatId}/messages

    Args:
        chat_id: Chat ID.
        page: Page number for pagination.
        page_size: Number of items per page.
    """
    result = await _client.get(
        f"/v2/chat/{chat_id}/messages",
        params={"page": page, "pageSize": page_size},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_all_chat_messages(chat_id: str) -> str:
    """Delete all messages in a chat (keeps the chat but clears history).

    DELETE /v2/chat/{chatId}/messages

    Args:
        chat_id: Chat ID.
    """
    result = await _client.delete(f"/v2/chat/{chat_id}/messages")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def send_chat_message(
    chat_id: str,
    message: Optional[str] = None,
    reply_message_id: Optional[str] = None,
    image: Optional[str] = None,
    audio: Optional[str] = None,
    video: Optional[str] = None,
    document: Optional[str] = None,
    document_name: Optional[str] = None,
    document_mimetype: Optional[str] = None,
) -> str:
    """Send a message in a chat. Supports text, image, audio, video, or document.

    POST /v2/chat/{chatId}/send-message

    Args:
        chat_id: Chat ID.
        message: Text message content.
        reply_message_id: ID of the message to reply to (for text messages).
        image: Image URL to send.
        audio: Audio URL to send.
        video: Video URL to send.
        document: Document URL to send.
        document_name: Document filename.
        document_mimetype: Document MIME type (e.g. application/pdf).
    """
    body: dict = {}
    if image:
        body["image"] = image
        if message:
            body["message"] = message
    elif audio:
        body["audio"] = audio
    elif video:
        body["video"] = video
    elif document:
        body["document"] = document
        if document_name:
            body["documentName"] = document_name
        if document_mimetype:
            body["documentMimetype"] = document_mimetype
    else:
        if message:
            body["message"] = message
        if reply_message_id:
            body["replyMessageId"] = reply_message_id

    result = await _client.post(f"/v2/chat/{chat_id}/send-message", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_chat_message(chat_id: str, message_id: str) -> str:
    """Delete a specific message from a chat.

    DELETE /v2/chat/{chatId}/message/{messageId}

    Args:
        chat_id: Chat ID.
        message_id: Message ID.
    """
    result = await _client.delete(f"/v2/chat/{chat_id}/message/{message_id}")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_chat_message(chat_id: str, message_id: str, message: Optional[str] = None) -> str:
    """Edit the text content of a message.

    PUT /v2/chat/{chatId}/message/{messageId}

    Args:
        chat_id: Chat ID.
        message_id: Message ID.
        message: New text content for the message.
    """
    result = await _client.put(
        f"/v2/chat/{chat_id}/message/{message_id}",
        json={"message": message},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def start_human_support(chat_id: str) -> str:
    """Transfer a chat to human support (pause the AI agent).

    PUT /v2/chat/{chatId}/start-human

    Args:
        chat_id: Chat ID.
    """
    result = await _client.put(f"/v2/chat/{chat_id}/start-human")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def stop_human_support(chat_id: str) -> str:
    """Resume AI agent for a chat (stop human support mode).

    PUT /v2/chat/{chatId}/stop-human

    Args:
        chat_id: Chat ID.
    """
    result = await _client.put(f"/v2/chat/{chat_id}/stop-human")
    return json.dumps(result, indent=2, ensure_ascii=False)
