from flask import Flask, request, jsonify
from mcp_adapter import handle_mcp_request

app = Flask(__name__)

@app.route("/n8n/chat", methods=["POST"])
def chat_webhook():
    """
    n8n webhook endpoint for Trojan Chat.
    Supports 'send_message' and 'fetch_messages'.
    """
    try:
        payload = request.get_json(force=True)
        tool_name = payload.get("tool")
        input_data = payload.get("input", {})

        result = handle_mcp_request(tool_name, input_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
