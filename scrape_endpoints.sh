#!/bin/bash

# Array of endpoint paths from llms.txt
endpoints=(
  "channels/create-channel"
  "channels/create-channel-workspace"
  "channels/edit-channel"
  "channels/edit-channel-config"
  "channels/list-channel-config"
  "channels/list-channels"
  "channels/list-channels2"
  "channels/qr-code"
  "channels/remove-channel"
  "channels/start-conversation"
  "channels/widget/get-links"
  "channels/widget/update-settings"
  "chats/delete-chat"
  "chats/delete-message"
  "chats/delete-messages"
  "chats/edit-message"
  "chats/list-chats"
  "chats/list-messages"
  "chats/send-message"
  "chats/start-human"
  "chats/stop-human"
  "contacts/create-contact"
  "contacts/edit-contact"
  "contacts/export-contacts"
  "contacts/get-contact"
  "contacts/import-contacts"
  "contacts/list-contacts"
  "contacts/remove-contact"
  "custom-fields/create"
  "custom-fields/delete"
  "custom-fields/edit"
  "custom-fields/get-fields"
  "idle-actions/create"
  "idle-actions/delete"
  "idle-actions/edit"
  "idle-actions/list"
  "intentions/create"
  "intentions/delete"
  "intentions/edit"
  "intentions/get"
  "intentions/list"
  "interactions/list"
  "mcp/create"
  "mcp/delete"
  "mcp/edit"
  "mcp/list"
  "trainings/create"
  "trainings/delete"
  "trainings/edit"
  "trainings/get"
  "trainings/list"
  "transfer-rules/create"
  "transfer-rules/delete"
  "transfer-rules/edit"
  "transfer-rules/list"
  "workspace/get-workspace"
  "workspace/list-workspaces"
)

declare -A endpoint_data

for endpoint in "${endpoints[@]}"; do
  url="https://developer.gptmaker.ai/${endpoint}.md"
  
  # Fetch the endpoint documentation
  response=$(curl -s "$url")
  
  # Check if we got a valid response (not 404)
  http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  
  if [ "$http_code" = "200" ]; then
    # Extract HTTP method and path from the markdown content
    # Looking for patterns like "GET /v2/..." or "POST /v2/..." etc.
    method=$(echo "$response" | grep -oE "^\`(GET|POST|PUT|DELETE|PATCH)" | head -1 | sed 's/`//g' | awk '{print $1}')
    path=$(echo "$response" | grep -oE "/v2/[^\`]+" | head -1)
    
    if [ -n "$method" ] && [ -n "$path" ]; then
      endpoint_data["$endpoint"]="$method $path"
      echo "[OK] $endpoint: $method $path"
    else
      echo "[PARTIAL] $endpoint: Found but couldn't extract method/path"
    fi
  else
    echo "[404] $endpoint: Documentation not found (HTTP $http_code)"
  fi
done

# Summary
echo ""
echo "=== SUMMARY ==="
found=0
notfound=0
for endpoint in "${!endpoint_data[@]}"; do
  ((found++))
done
for endpoint in "${endpoints[@]}"; do
  if [ -z "${endpoint_data[$endpoint]}" ]; then
    ((notfound++))
  fi
done

echo "Found: $found endpoints"
echo "Not found (404): $notfound endpoints"

