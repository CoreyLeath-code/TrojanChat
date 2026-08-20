import json
from datetime import datetime, timezone
from typing import Dict, Any, List

# Example in-memory storage (replace with DB later)
CHAT_HISTORY = {
    "game-day": [],
    "recruiting": [],
    "staff": []
}


def send_message(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a message to a chat room (MCP-compatible).
    """
    room = input_data.get("room")
    user = input_data.get("user")
    message = input_data.get("message")

    if room not in CHAT_HISTORY:
        return {"status": "failed", "timestamp": datetime.now(timezone.utc).isoformat()}

    entry = {
        "user": user,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    CHAT_HISTORY[room].append(entry)

    return {"status": "sent", "timestamp": entry["timestamp"]}


def fetch_messages(input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Fetch recent messages from a chat room (MCP-compatible).
    """
    room = input_data.get("room")
    limit = input_data.get("limit", 10)

    if room not in CHAT_HISTORY:
        return []

    return CHAT_HISTORY[room][-limit:]


def handle_mcp_request(tool_name: str, input_payload: Dict[str, Any]) -> Any:
    """
    Dispatcher for MCP tool requests.
    """
    if tool_name == "send_message":
        return send_message(input_payload)
    elif tool_name == "fetch_messages":
        return fetch_messages(input_payload)
    else:
        return {"error": f"Unknown tool: {tool_name}"}


if __name__ == "__main__":
    # Example test
    test_send = handle_mcp_request("send_message", {
        "room": "game-day",
        "user": "Corey",
        "message": "Fight On! Welcome to the new season kickoff!"
    })

    print("Send Result:", json.dumps(test_send, indent=2))

    test_fetch = handle_mcp_request("fetch_messages", {
        "room": "game-day",
        "limit": 5
    })

    print("Fetch Result:", json.dumps(test_fetch, indent=2))
