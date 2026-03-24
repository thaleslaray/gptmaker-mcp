"""GPTMaker tools — Custom Fields."""

import json
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()


async def list_custom_fields(
    workspace_id: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    query: Optional[str] = None,
) -> str:
    """List all custom fields in a workspace.

    GET /v2/custom-field/workspace/{workspaceId}

    Args:
        workspace_id: Workspace ID.
        page: Page number for pagination.
        page_size: Number of items per page.
        query: Search query to filter fields by name.
    """
    result = await _client.get(
        f"/v2/custom-field/workspace/{workspace_id}",
        params={"page": page, "pageSize": page_size, "query": query},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


async def create_custom_field(
    workspace_id: str,
    name: Optional[str] = None,
    json_name: Optional[str] = None,
    description: Optional[str] = None,
    type_: Optional[str] = None,
) -> str:
    """Create a new custom field in a workspace.

    POST /v2/custom-field/workspace/{workspaceId}

    Args:
        workspace_id: Workspace ID.
        name: Display name of the custom field.
        json_name: JSON key name for the field (snake_case recommended).
        description: Description of what this field stores.
        type_: Field data type. Values: STRING, DATE, DATE_TIME, NUMBER, BOOLEAN, MONEY.
    """
    body = {
        "name": name,
        "jsonName": json_name,
        "description": description,
        "type": type_,
    }
    result = await _client.post(f"/v2/custom-field/workspace/{workspace_id}", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def update_custom_field(
    customfield_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    type_: Optional[str] = None,
    json_name: Optional[str] = None,
) -> str:
    """Update an existing custom field.

    PUT /v2/custom-field/{customfieldId}

    Args:
        customfield_id: Custom field ID.
        name: New display name.
        description: New description.
        type_: New data type. Values: STRING, DATE, DATE_TIME, NUMBER, BOOLEAN, MONEY.
        json_name: New JSON key name.
    """
    body = {
        "name": name,
        "description": description,
        "type": type_,
        "jsonName": json_name,
    }
    result = await _client.put(f"/v2/custom-field/{customfield_id}", json=body)
    return json.dumps(result, indent=2, ensure_ascii=False)


async def toggle_archive_custom_field(
    customfield_id: str,
    archived: Optional[bool] = None,
) -> str:
    """Archive or unarchive a custom field.

    PUT /v2/custom-field/toggle-archive/{customfieldId}

    Args:
        customfield_id: Custom field ID.
        archived: True to archive, False to unarchive.
    """
    result = await _client.put(
        f"/v2/custom-field/toggle-archive/{customfield_id}",
        json={"archived": archived},
    )
    return json.dumps(result, indent=2, ensure_ascii=False)
