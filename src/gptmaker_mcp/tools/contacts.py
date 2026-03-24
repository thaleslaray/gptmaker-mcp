"""GPTMaker tools — Contacts."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def search_contacts(
    workspace_id: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
) -> str:
    """Search contacts in a workspace.

    GET /v2/workspace/{workspaceId}/search

    Args:
        workspace_id: Workspace ID.
        page: Page number for pagination.
        page_size: Number of items per page.
    """
    result = await _client.get(
        f"/v2/workspace/{workspace_id}/search",
        params={"page": page, "pageSize": page_size},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def get_contact(workspace_id: str, contact_id: str) -> str:
    """Get a specific contact by ID within a workspace.

    GET /v2/workspace/{workspaceId}/contact/{contactId}

    Args:
        workspace_id: Workspace ID.
        contact_id: Contact ID.
    """
    result = await _client.get(f"/v2/workspace/{workspace_id}/contact/{contact_id}")
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_contact(
    contact_id: str,
    name: Optional[str] = None,
    birthday: Optional[int] = None,
    gender: Optional[str] = None,
    picture: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    job_title: Optional[str] = None,
    recipient: Optional[str] = None,
    custom_field_values: Optional[list] = None,
) -> str:
    """Update a contact's information.

    PUT /v2/contact/{contactId}/update

    Args:
        contact_id: Contact ID.
        name: Contact full name.
        birthday: Birthday as Unix timestamp (milliseconds).
        gender: Gender. Values: MALE, FEMALE, OTHER.
        picture: Profile picture URL.
        phone: Phone number.
        email: Email address.
        job_title: Job title or profession.
        recipient: Recipient identifier.
        custom_field_values: Array of custom field values [{fieldId, value}].
    """
    body = {
        "name": name,
        "birthday": birthday,
        "gender": gender,
        "picture": picture,
        "phone": phone,
        "email": email,
        "jobTitle": job_title,
        "recipient": recipient,
        "customFieldValues": custom_field_values,
    }
    result = await _client.put(f"/v2/contact/{contact_id}/update", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)
