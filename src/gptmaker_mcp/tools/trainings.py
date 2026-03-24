"""GPTMaker tools — Trainings."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def list_trainings(
    agent_id: str,
    type_: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    query: Optional[str] = None,
) -> str:
    """List trainings for an agent filtered by type.

    GET /v2/agent/{agentId}/trainings

    Args:
        agent_id: Agent ID.
        type_: Training type (required). Values: TEXT, WEBSITE, VIDEO, DOCUMENT.
        page: Page number for pagination.
        page_size: Number of items per page.
        query: Search query to filter trainings.
    """
    result = await _client.get(
        f"/v2/agent/{agent_id}/trainings",
        params={"type": type_, "page": page, "pageSize": page_size, "query": query},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def create_training(
    agent_id: str,
    type_: str,
    text: Optional[str] = None,
    image: Optional[str] = None,
    website: Optional[str] = None,
    training_sub_pages: Optional[str] = None,
    training_interval: Optional[str] = None,
    video: Optional[str] = None,
    document_url: Optional[str] = None,
    document_name: Optional[str] = None,
    document_mimetype: Optional[str] = None,
    callback_url: Optional[str] = None,
) -> str:
    """Create a new training for an agent. Supports text, website, video, or document.

    POST /v2/agent/{agentId}/trainings

    Args:
        agent_id: Agent ID.
        type_: Training type. Values: TEXT, WEBSITE, VIDEO, DOCUMENT.
        text: Text content for TEXT type training.
        image: Optional image URL for TEXT type training.
        website: Website URL for WEBSITE type training.
        training_sub_pages: Whether to crawl sub-pages for WEBSITE type. Values: true, false.
        training_interval: Re-crawl interval for WEBSITE type. Values: DAILY, WEEKLY, MONTHLY.
        video: Video URL for VIDEO type training.
        document_url: Document URL for DOCUMENT type training.
        document_name: Document filename for DOCUMENT type training.
        document_mimetype: MIME type of the document (e.g. application/pdf).
        callback_url: Webhook URL to receive training completion notification.
    """
    body: dict = {"type": type_}
    if type_ == "TEXT":
        if text:
            body["text"] = text
        if image:
            body["image"] = image
    elif type_ == "WEBSITE":
        if website:
            body["website"] = website
        if training_sub_pages:
            body["trainingSubPages"] = training_sub_pages
        if training_interval:
            body["trainingInterval"] = training_interval
    elif type_ == "VIDEO":
        if video:
            body["video"] = video
    elif type_ == "DOCUMENT":
        if document_url:
            body["documentUrl"] = document_url
        if document_name:
            body["documentName"] = document_name
        if document_mimetype:
            body["documentMimetype"] = document_mimetype
    if callback_url:
        body["callbackUrl"] = callback_url

    result = await _client.post(f"/v2/agent/{agent_id}/trainings", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_training(
    training_id: str,
    type_: Optional[str] = None,
    text: Optional[str] = None,
    image: Optional[str] = None,
) -> str:
    """Update an existing text training.

    PUT /v2/training/{trainingId}

    Args:
        training_id: Training ID.
        type_: Training type. Values: TEXT.
        text: Updated text content.
        image: Updated image URL.
    """
    body = {"type": type_, "text": text, "image": image}
    result = await _client.put(f"/v2/training/{training_id}", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def delete_training(training_id: str) -> str:
    """Delete a training.

    DELETE /v2/training/{trainingId}

    Args:
        training_id: Training ID.
    """
    result = await _client.delete(f"/v2/training/{training_id}")
    return json.dumps(result, indent=2, ensure_ascii=False)
