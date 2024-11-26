from pydantic_settings import BaseSettings
from typing import Optional
import json

class Settings(BaseSettings):
    # Hugging Face
    HUGGINGFACE_TOKEN: str

    # Firebase
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_CLIENT_ID: Optional[str] = None
    FIREBASE_AUTH_URI: str = "https://accounts.google.com/o/oauth2/auth"
    FIREBASE_TOKEN_URI: str = "https://oauth2.googleapis.com/token"
    FIREBASE_AUTH_PROVIDER_CERT_URL: str = "https://www.googleapis.com/oauth2/v1/certs"
    FIREBASE_CLIENT_CERT_URL: Optional[str] = None

    class Config:
        env_file = ".env"

    def get_firebase_credentials(self) -> dict:
        """Generate Firebase credentials dictionary from environment variables."""
        return {
            "type": "service_account",
            "project_id": self.FIREBASE_PROJECT_ID,
            "private_key_id": self.FIREBASE_PRIVATE_KEY_ID,
            "private_key": self.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
            "client_email": self.FIREBASE_CLIENT_EMAIL
        }

    def validate(self) -> None:
        """Validate the configuration settings."""
        if not self.HUGGINGFACE_TOKEN:
            raise ValueError("HUGGINGFACE_TOKEN is required")
        
        required_firebase_fields = [
            "FIREBASE_PROJECT_ID",
            "FIREBASE_PRIVATE_KEY_ID",
            "FIREBASE_PRIVATE_KEY",
            "FIREBASE_CLIENT_EMAIL"
        ]
        
        missing_fields = [field for field in required_firebase_fields if not getattr(self, field)]
        if missing_fields:
            raise ValueError(f"Missing required Firebase fields: {', '.join(missing_fields)}")
        
        try:
            # Validate private key format
            if not self.FIREBASE_PRIVATE_KEY.startswith("-----BEGIN PRIVATE KEY-----"):
                raise ValueError("Invalid FIREBASE_PRIVATE_KEY format")
        except Exception as e:
            raise ValueError(f"Invalid Firebase credentials format: {str(e)}")
