# gptmaker-mcp

MCP server for the [GPTMaker](https://app.gptmaker.ai) API. Manage AI agents, channels, chats, trainings, intentions, transfer rules, and more — directly from Claude Code or any MCP-compatible client.

## Installation

```bash
pip install gptmaker-mcp
```

## Setup

Get your API token from [app.gptmaker.ai/browse/developers](https://app.gptmaker.ai/browse/developers), then add the MCP server to Claude Code:

```bash
claude mcp add gptmaker -e GPTMAKER_API_TOKEN=your_token_here -- gptmaker-mcp
```

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
| **Intentions** | Configure webhook triggers (CRM integrations, automations) |
| **Transfer Rules** | Set up conditional conversation transfers |
| **Idle Actions** | Configure automatic follow-up sequences |
| **MCP Connections** | Connect external MCP servers to agents |
| **Diagnostics** | Full agent health audit with scoring |

## Requirements

- Python 3.11+
- GPTMaker account with API token

## License

MIT
