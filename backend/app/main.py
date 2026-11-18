"""Compatibility entrypoint for the single supported TrojanChat ASGI application.

The canonical implementation lives in backend.api and includes validated chat
and websocket routes. Reuse it rather than registering a second, divergent
application with duplicate routes and permissive credentialed CORS.
"""

from backend.api import app

__all__ = ["app"]
