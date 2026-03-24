#!/bin/bash
echo "GPTMaker MCP — Instalação"
echo ""
read -p "Cole seu token do GPTMaker: " token
claude mcp add gptmaker -e "GPTMAKER_API_TOKEN=$token" -- uvx gptmaker-mcp
echo ""
echo "Pronto! Reinicie o Claude Code."
