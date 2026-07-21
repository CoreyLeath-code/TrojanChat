import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Centralized configuration for the TrojanChat backend.
    This allows clean environment separation and avoids hardcoding.
    """

    # App Settings
    APP_NAME: str = "TrojanChat Backend"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Backend API Version
    API_VERSION: str = "v1"

    # Local development settings
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "10000"))

settings = Settings()
