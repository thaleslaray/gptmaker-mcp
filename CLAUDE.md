# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -e ".[dev]"          # or: uv pip install -e ".[dev]"

# Run the server (stdio transport, default for MCP)
gptmaker-mcp

# Run with inspector for debugging
fastmcp dev src/gptmaker_mcp/server.py

# Run the server with HTTP transport
fastmcp run src/gptmaker_mcp/server.py --transport http

# Auth: set before running
export GPTMAKER_API_TOKEN=your_token_here
```

## Architecture

This is a **FastMCP server** that wraps the GPTMaker API (`https://api.gptmaker.ai`). The MCP protocol runs over stdio (default) or HTTP.

### Tool registration

`server.py` auto-discovers and registers all tools via reflection: it scans `src/gptmaker_mcp/tools/*.py`, finds every public async function, and registers each as an MCP tool with `mcp.tool()`. **Any public async function in a tools module is automatically exposed as an MCP tool.** Private helpers must be prefixed with `_`.

The server also enables `CodeMode` (FastMCP's code execution transform) via a MontySandbox.

### HTTP client

`client.py` contains `GptMakerClient` — a singleton-style async httpx client shared across tools. Key behaviors:
- Reads `GPTMAKER_API_TOKEN` from env at instantiation
- Lazy connection pooling (reconnects if closed)
- 3 retries with exponential backoff on HTTP 429
- `None` values in params/json are stripped before the request

Each tool module creates its own `_client = GptMakerClient()` instance at module level. This is intentional — the underlying httpx client is reused via connection pooling.

### Tool modules

| Module | Covers |
|--------|--------|
| `workspace.py` | List workspaces, credits |
| `agents.py` | CRUD, settings, webhooks, activate/deactivate, chat |
| `trainings.py` | Text, website, video, document trainings |
| `channels.py` | CRUD, QR code, widget, config, conversations |
| `chats.py` | List chats/messages, send messages, human handoff |
| `contacts.py` | Search, get, update contacts |
| `custom_fields.py` | Workspace custom fields |
| `idle_actions.py` | Automatic idle message sequences |
| `intentions.py` | Webhook triggers for agents |
| `transfer_rules.py` | Conversation transfer conditions |
| `interactions.py` | Completed interactions, CSV export |
| `mcp_connections.py` | Add/manage MCP server connections for agents |
| `composites.py` | Higher-level tools built on primitives (see below) |
| `diagnostics.py` | `audit_agent` — full health check with scoring |

### Composite tools (composites.py)

These are orchestration-level tools that call multiple API endpoints:

- `get_workspace_summary` — parallel-fetches agents, channels, and credits in one call
- `find_chat_by_phone` — paginates through contacts with exact phone normalization to locate a chat
- `monitor_channel_health` — checks all channels for connectivity status
- `bulk_update_agent_model` — migrates all agents from one LLM model to another (supports `dry_run`)
- `bulk_send_messages` — outbound message blast with per-send delay (Z-API/Evolution only)
- `setup_notification_alerts` — configures webhook URLs for multiple agent events atomically

### API conventions

- All API paths are `/v2/...`
- IDs may come back as `id` or `_id` — code always checks both: `a.get("id") or a.get("_id")`
- List endpoints return either a bare list or `{"data": [...]}` or `{"items": [...]}` — code normalizes all three patterns
- Phone numbers are normalized by stripping `+`, spaces, and dashes; last 9 digits used as fallback suffix for matching
