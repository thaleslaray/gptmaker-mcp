# gptmaker-mcp

MCP server for the [GPTMaker](https://app.gptmaker.ai) API. Manage AI agents, channels, chats, trainings, intentions, transfer rules, and more — directly from Claude Code or any MCP-compatible client.

## Installation

### Claude Code (recommended)

**Step 1** — add your token to `~/.zshrc` (or `~/.bashrc`):

```bash
echo 'export GPTMAKER_API_TOKEN=your_token_here' >> ~/.zshrc
source ~/.zshrc
```

**Step 2** — add the MCP server:

```bash
claude mcp add gptmaker -- uvx gptmaker-mcp
```

That's it. No need to install anything manually — `uvx` fetches and runs the package on demand.

### Other MCP clients (Cursor, Windsurf, etc.)

Add to your MCP config:

```json
{
  "mcpServers": {
    "gptmaker": {
      "command": "uvx",
      "args": ["gptmaker-mcp"],
      "env": {
        "GPTMAKER_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Setup

Get your API token at [app.gptmaker.ai/browse/developers](https://app.gptmaker.ai/browse/developers).

## What it does

Exposes the full GPTMaker API as MCP tools:

| Group | Tools |
|-------|-------|
| **Workspace** | List workspaces, check credits |
| **Agents** | Create, read, update, delete agents; configure settings, behavior, webhooks; activate/deactivate; chat |
| **Trainings** | Add text, website, video, and document trainings |
| **Channels** | Manage WhatsApp/Instagram channels, QR codes, widget config |
| **Chats** | List conversations, send messages, human handoff |
| **Contacts** | Search, get, update contacts |
| **Custom Fields** | CRUD for workspace custom fields |
| **Intentions** | Configure webhook triggers (CRM integrations, automations) |
| **Transfer Rules** | Set up conditional conversation transfers |
| **Idle Actions** | Configure automatic follow-up sequences |
| **Interactions** | List completed interactions, export to CSV |
| **MCP Connections** | Connect external MCP servers to agents |
| **Diagnostics** | Full agent health audit with scoring |

### Composite tools

Higher-level tools that orchestrate multiple API calls:

| Tool | What it does |
|------|-------------|
| `get_workspace_summary` | Fetches agents, channels, and credits in a single call |
| `find_chat_by_phone` | Locates a conversation by phone number |
| `monitor_channel_health` | Checks connectivity status of all channels |
| `bulk_update_agent_model` | Migrates all agents from one LLM model to another |
| `bulk_send_messages` | Sends outbound messages to multiple contacts |
| `setup_notification_alerts` | Configures webhook URLs for multiple agent events atomically |

## Code execution (CodeMode)

This server includes **CodeMode** — a sandboxed Python execution environment. Claude can write and run Python code directly within the MCP session to automate bulk operations, data transformations, or any task that benefits from scripting.

## Requirements

- Python 3.11+
- GPTMaker account with API token

## License

MIT
