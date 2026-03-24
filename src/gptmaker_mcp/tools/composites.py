"""GPTMaker tools — Composite tools built on top of primitives."""

import asyncio
import json
import time
from typing import Optional

from gptmaker_mcp.client import GptMakerClient

_client = GptMakerClient()

# Webhook event field names
WEBHOOK_EVENTS = {
    "new_message": "onNewMessage",
    "lack_knowledge": "onLackKnowLedge",
    "first_interaction": "onFirstInteraction",
    "start_interaction": "onStartInteraction",
    "transfer": "onTransfer",
    "finish_interaction": "onFinishInteraction",
    "create_event": "onCreateEvent",
    "cancel_event": "onCancelEvent",
}


async def get_workspace_summary() -> str:
    """Get a complete overview of the current workspace: ID, agents, channels, and credits.

    Returns a human-readable summary with IDs, statuses, and credit balance.
    Useful as a first step to discover IDs needed for other operations.
    """
    workspaces = await _client.get("/v2/workspaces")
    if not workspaces:
        return json.dumps({"error": "No workspaces found."}, ensure_ascii=False)

    workspace = workspaces[0]
    workspace_id = workspace.get("id") or workspace.get("_id", "")
    workspace_name = workspace.get("name", "Unknown")

    agents_data, channels_data, credits_data = await asyncio.gather(
        _client.get(f"/v2/workspace/{workspace_id}/agents"),
        _client.get(f"/v2/workspace/{workspace_id}/channels"),
        _client.get(f"/v2/workspace/{workspace_id}/credits"),
        return_exceptions=True,
    )

    agents = agents_data if isinstance(agents_data, list) else (agents_data or {}).get("data", [])
    channels = channels_data if isinstance(channels_data, list) else (channels_data or {}).get("data", [])
    credits_balance = credits_data if not isinstance(credits_data, Exception) else {}

    agent_lines = []
    for a in agents:
        status = "✅ Ativo" if a.get("active") else "⚠️  Inativo"
        agent_lines.append(f"  {status} | {a.get('name', 'Sem nome')} (ID: {a.get('id') or a.get('_id', '')})")

    channel_lines = []
    for c in channels:
        connected = c.get("connected", c.get("status") == "connected")
        status = "✅ Conectado" if connected else "❌ Desconectado"
        ctype = c.get("type", "")
        channel_lines.append(f"  {status} | {c.get('name', ctype)} (ID: {c.get('id') or c.get('_id', '')})")

    credits_info = ""
    if isinstance(credits_balance, dict):
        remaining = credits_balance.get("credits", credits_balance.get("remaining", "N/A"))
        credits_info = f"\nCréditos: {remaining}"

    summary = (
        f"Workspace: {workspace_name}\n"
        f"ID: {workspace_id}"
        f"{credits_info}\n"
        f"\nAgentes ({len(agents)}):\n" + ("\n".join(agent_lines) if agent_lines else "  Nenhum") +
        f"\n\nCanais ({len(channels)}):\n" + ("\n".join(channel_lines) if channel_lines else "  Nenhum")
    )

    return summary


async def find_chat_by_phone(workspace_id: str, phone: str) -> str:
    """Find a chat by the contact's phone number.

    Searches contacts and chats to locate the chatId associated with a phone number.
    Useful when you have a phone number but need the chatId to send messages.

    Args:
        workspace_id: Workspace ID.
        phone: Phone number to search (e.g. 5511999999999).
    """
    phone_normalized = phone.strip().lstrip("+").replace(" ", "").replace("-", "")
    suffix = phone_normalized[-9:]

    # Paginate through all contacts to find exact phone match
    contact = None
    page = 1
    while True:
        results = await _client.get(
            f"/v2/workspace/{workspace_id}/search",
            params={"query": phone_normalized, "page": page, "pageSize": 100},
        )
        batch = results if isinstance(results, list) else (results or {}).get("data", (results or {}).get("contacts", []))
        if not batch:
            break
        for c in batch:
            c_phone = (c.get("phone") or c.get("recipient") or "").replace("+", "").replace(" ", "")
            if c_phone == phone_normalized or c_phone.endswith(suffix):
                contact = c
                break
        if contact or len(batch) < 100:
            break
        page += 1

    if not contact:
        return json.dumps({"found": False, "message": f"No contact found with phone {phone}."}, ensure_ascii=False)

    contact_id = contact.get("id") or contact.get("_id", "")
    contact_name = contact.get("name", "Unknown")

    chats_data = await _client.get(
        f"/v2/workspace/{workspace_id}/chats",
        params={"query": phone, "pageSize": 10},
    )
    chats = chats_data if isinstance(chats_data, list) else (chats_data or {}).get("data", [])

    chat_match = None
    for chat in chats:
        chat_contact = chat.get("contact", {})
        if (
            chat_contact.get("phone", "") == phone
            or str(chat_contact.get("id") or chat_contact.get("_id", "")) == str(contact_id)
        ):
            chat_match = chat
            break

    if not chat_match and chats:
        chat_match = chats[0]

    if not chat_match:
        return json.dumps({
            "found": True,
            "contact_id": contact_id,
            "contact_name": contact_name,
            "chat_id": None,
            "message": "Contact found but no active chat.",
        }, ensure_ascii=False)

    chat_id = chat_match.get("id") or chat_match.get("_id", "")
    agent = chat_match.get("agent", {})
    last_message = chat_match.get("lastMessage", {})

    return json.dumps({
        "found": True,
        "chat_id": chat_id,
        "contact_id": contact_id,
        "contact_name": contact_name,
        "agent_name": agent.get("name", ""),
        "agent_id": agent.get("id") or agent.get("_id", ""),
        "last_message_at": last_message.get("createdAt", ""),
        "last_message_preview": str(last_message.get("message", ""))[:100],
    }, indent=2, ensure_ascii=False)


async def monitor_channel_health(workspace_id: str) -> str:
    """Check the connection status of all channels in a workspace.

    Returns a summary of which channels are online, offline, or unknown.
    Useful for detecting silently disconnected WhatsApp/Instagram channels.

    Args:
        workspace_id: Workspace ID.
    """
    channels_data = await _client.get(f"/v2/workspace/{workspace_id}/channels")
    channels = channels_data if isinstance(channels_data, list) else (channels_data or {}).get("data", [])

    if not channels:
        return "No channels found in this workspace."

    online, offline, unknown = [], [], []

    for c in channels:
        name = c.get("name") or c.get("type", "Unknown")
        cid = c.get("id") or c.get("_id", "")
        ctype = c.get("type", "")
        label = f"{name} [{ctype}] (ID: {cid})"

        connected = c.get("connected")
        status = c.get("status", "")

        if connected is True or status == "connected":
            online.append(f"  ✅ {label}")
        elif connected is False or status in ("disconnected", "offline"):
            offline.append(f"  ❌ {label}")
        else:
            unknown.append(f"  ❓ {label}")

    lines = [f"Channel Health — {len(channels)} total\n"]
    if offline:
        lines.append(f"OFFLINE ({len(offline)}):")
        lines.extend(offline)
        lines.append("  → Action needed: reconnect these channels.\n")
    if online:
        lines.append(f"Online ({len(online)}):")
        lines.extend(online)
    if unknown:
        lines.append(f"\nUnknown status ({len(unknown)}):")
        lines.extend(unknown)

    return "\n".join(lines)


async def bulk_update_agent_model(
    workspace_id: str,
    from_model: str,
    to_model: str,
    dry_run: bool = False,
) -> str:
    """Find all agents using a specific LLM model and update them to a new model in bulk.

    Useful for migrating agents away from deprecated models (e.g. CLAUDE_3_5_HAIKU → CLAUDE_HAIKU_4_5).

    Args:
        workspace_id: Workspace ID.
        from_model: Current model identifier to search for (e.g. CLAUDE_3_5_HAIKU).
        to_model: New model identifier to set (e.g. CLAUDE_HAIKU_4_5).
        dry_run: If True, only report which agents would be updated without making changes.
    """
    agents_data = await _client.get(f"/v2/workspace/{workspace_id}/agents")
    agents = agents_data if isinstance(agents_data, list) else (agents_data or {}).get("data", [])

    if not agents:
        return "No agents found in this workspace."

    settings_results = await asyncio.gather(
        *[_client.get(f"/v2/agent/{a.get('id') or a.get('_id')}/settings") for a in agents],
        return_exceptions=True,
    )

    targets = []
    for agent, settings in zip(agents, settings_results):
        if isinstance(settings, Exception):
            continue
        current_model = settings.get("prefferModel", settings.get("llmModel", settings.get("model", "")))
        if current_model == from_model:
            targets.append((agent, settings))

    if not targets:
        return f"No agents found using model '{from_model}'."

    lines = [f"Agents using '{from_model}': {len(targets)}\n"]

    if dry_run:
        lines.append("DRY RUN — no changes made:\n")
        for agent, _ in targets:
            lines.append(f"  · {agent.get('name', 'Unknown')} (ID: {agent.get('id') or agent.get('_id')})")
        return "\n".join(lines)

    update_results = await asyncio.gather(
        *[
            _client.put(
                f"/v2/agent/{a.get('id') or a.get('_id')}/settings",
                json={**s, "prefferModel": to_model},
            )
            for a, s in targets
        ],
        return_exceptions=True,
    )

    ok, failed = 0, 0
    for (agent, _), result in zip(targets, update_results):
        name = agent.get("name", "Unknown")
        aid = agent.get("id") or agent.get("_id")
        if isinstance(result, Exception):
            lines.append(f"  ❌ {name} (ID: {aid}) — error: {result}")
            failed += 1
        else:
            lines.append(f"  ✅ {name} (ID: {aid}) — updated")
            ok += 1

    lines.append(f"\nDone: {ok} updated, {failed} failed.")
    return "\n".join(lines)


async def bulk_send_messages(
    channel_id: str,
    phones: list[str],
    message: str,
    delay_seconds: float = 5.0,
) -> str:
    """Send a message to a list of phone numbers via a channel (outbound).

    Uses start_conversation for each number. Only works with unofficial WhatsApp channels (Z-API/Evolution).
    Adds a configurable delay between sends to avoid spam detection.

    Args:
        channel_id: Channel ID to send from (must be unofficial WhatsApp type).
        phones: List of phone numbers to send to (e.g. ["5511999999999", "5521888888888"]).
        message: Message text to send.
        delay_seconds: Seconds to wait between each send (default: 5).
    """
    if not phones:
        return "No phone numbers provided."

    results = []
    ok, failed = 0, 0

    for i, phone in enumerate(phones):
        try:
            await _client.post(
                f"/v2/channel/{channel_id}/start-conversation",
                json={"phone": phone, "message": message},
            )
            results.append(f"  ✅ {phone}")
            ok += 1
        except Exception as e:
            results.append(f"  ❌ {phone} — {e}")
            failed += 1

        if i < len(phones) - 1:
            time.sleep(delay_seconds)

    lines = [f"Bulk send — {len(phones)} numbers\n"]
    lines.extend(results)
    lines.append(f"\nDone: {ok} sent, {failed} failed.")
    return "\n".join(lines)


async def setup_notification_alerts(
    agent_id: str,
    webhook_url: str,
    events: Optional[list[str]] = None,
) -> str:
    """Configure webhook notifications for agent events.

    Sets the given URL to receive POST requests for selected events.
    Existing webhooks for other events are preserved.

    Available events:
        - new_message: A new message arrives in any chat
        - lack_knowledge: Agent doesn't know how to answer
        - first_interaction: First ever interaction with a contact
        - start_interaction: Any new interaction starts
        - transfer: Agent transfers to human support
        - finish_interaction: Interaction is finished
        - create_event: A new appointment/event is created
        - cancel_event: An appointment/event is cancelled

    Args:
        agent_id: Agent ID.
        webhook_url: URL to receive the webhook POST requests.
        events: List of event names to configure (default: all events).
    """
    if events is None:
        events = list(WEBHOOK_EVENTS.keys())

    invalid = [e for e in events if e not in WEBHOOK_EVENTS]
    if invalid:
        valid_list = ", ".join(WEBHOOK_EVENTS.keys())
        return f"Invalid events: {invalid}. Valid options: {valid_list}"

    current = await _client.get(f"/v2/agent/{agent_id}/webhooks")
    payload = dict(current) if isinstance(current, dict) else {}

    configured = []
    for event in events:
        field = WEBHOOK_EVENTS[event]
        payload[field] = webhook_url
        configured.append(f"  ✅ {event} → {field}")

    await _client.put(f"/v2/agent/{agent_id}/webhooks", json=payload)

    lines = [f"Notification alerts configured for agent {agent_id}\n"]
    lines.append(f"URL: {webhook_url}\n")
    lines.append("Events configured:")
    lines.extend(configured)
    lines.append(f"\nAll {len(configured)} event(s) will POST to the URL above.")
    return "\n".join(lines)
