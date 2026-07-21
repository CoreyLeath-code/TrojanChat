import datetime
import os
import threading
import uuid
from collections import deque
from datetime import timezone


class ChatService:
    """
    Chat service responsible for sending and retrieving messages.
    Currently uses in-memory storage, but the class is designed
    to be upgraded easily to Firebase, Redis, or SQL.
    """

    def __init__(self, max_messages: int | None = None):
        """Create a bounded, thread-safe store for one process.

        A durable shared store is still required for multi-instance production deployments.
        """
        configured_limit = max_messages or int(os.getenv("CHAT_HISTORY_LIMIT", "10000"))
        if configured_limit < 1:
            raise ValueError("max_messages must be positive")
        self.messages = deque(maxlen=configured_limit)
        self._lock = threading.RLock()

    def _generate_message_id(self):
        """
        Creates a unique message ID using UUID4.
        """
        return str(uuid.uuid4())

    def _timestamp(self):
        """
        Returns an ISO 8601 timestamp.
        """
        return datetime.datetime.now(timezone.utc).isoformat()

    # -------------------------------------
    #  PUBLIC METHODS
    # -------------------------------------

    def send_message(self, username: str, content: str):
        """
        Stores a chat message and returns the structured message.
        """
        message = {
            "id": self._generate_message_id(),
            "username": username,
            "content": content,
            "timestamp": self._timestamp(),
        }

        # In-memory storage (can replace with Firebase/Postgres/etc.)
        with self._lock:
            self.messages.append(message)

        return message

    def get_messages(self, limit: int = 50):
        """
        Returns the latest 'limit' chat messages.
        """
        if limit < 1:
            return []
        with self._lock:
            return list(self.messages)[-limit:]
