"""GPTMaker MCP server — entry point."""

import importlib
import inspect
from pathlib import Path

from fastmcp import FastMCP
from fastmcp.experimental.transforms.code_mode import CodeMode, MontySandboxProvider

mcp = FastMCP(
    "gptmaker",
    instructions=(
        "GPTMaker API — manage AI agents, channels, chats, contacts, trainings, "
        "intentions, transfer rules, idle actions, custom fields, interactions, "
        "and MCP connections.\n\n"
        "Available tool groups:\n"
        "- workspace: list workspaces, get credits\n"
        "- agents: CRUD, settings, webhooks, activate/deactivate, chat, credits, behavior history\n"
        "- trainings: create/list/update/delete text, website, video, document trainings\n"
        "- channels: create/list/update/delete channels, QR code, widget, config, conversations\n"
        "- chats: list chats and messages, send messages, human support handoff\n"
        "- contacts: search, get, update contacts\n"
        "- custom_fields: CRUD for workspace custom fields\n"
        "- idle_actions: configure automatic idle message sequences\n"
        "- intentions: configure webhook triggers for agents\n"
        "- transfer_rules: configure conversation transfer conditions\n"
        "- interactions: list/delete completed interactions, export to CSV\n"
        "- mcp_connections: add/manage MCP server connections for agents\n\n"
        "Auth: set GPTMAKER_API_TOKEN environment variable."
    ),
)


def _register_tools() -> None:
    tools_dir = Path(__file__).parent / "tools"
    for module_path in sorted(tools_dir.glob("*.py")):
        if module_path.stem == "__init__":
            continue
        module = importlib.import_module(f"gptmaker_mcp.tools.{module_path.stem}")
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if inspect.iscoroutinefunction(obj) and not name.startswith("_"):
                mcp.tool(obj)


_register_tools()

sandbox = MontySandboxProvider(
    limits={"max_duration_secs": 30, "max_memory": 100_000_000},
)
mcp.add_transform(CodeMode(sandbox_provider=sandbox))


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
