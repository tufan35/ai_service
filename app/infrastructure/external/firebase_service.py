from firebase_admin import auth, credentials, initialize_app, get_app
import os
from app.domain.entities.auth import User, TokenVerification
from app.domain.repositories.auth_repository import AuthRepository
import logging

class FirebaseService(AuthRepository):
    def __init__(self):
        try:
            firebase_credentials = {
                "type": "service_account",
                "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n') if os.getenv("FIREBASE_PRIVATE_KEY") else None,
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
            }

            logging.info("Firebase credentials loaded: %s", firebase_credentials)

            required_vars = [
                "FIREBASE_PROJECT_ID", "FIREBASE_PRIVATE_KEY_ID", 
                "FIREBASE_PRIVATE_KEY", "FIREBASE_CLIENT_EMAIL"
            ]

            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                raise ValueError(f"Missing required Firebase environment variables: {', '.join(missing_vars)}")

            try:
                app = get_app()
                logging.info("Using existing Firebase app")
            except ValueError:
                cred = credentials.Certificate(firebase_credentials)
                initialize_app(cred)
                logging.info("Firebase initialized successfully")

        except Exception as e:
            logging.error("Error initializing Firebase: %s", str(e))
            raise

    async def verify_token(self, token_verification: TokenVerification) -> User:
        try:
            logging.info("Attempting to verify token")
            decoded_token = auth.verify_id_token(token_verification.id_token)
            logging.info("Token decoded successfully: %s", decoded_token)
            
            user_info = auth.get_user(decoded_token['uid'])
            logging.info("User info retrieved: %s", user_info)
            
            return User(
                uid=user_info.uid,
                email=user_info.email,
                display_name=user_info.display_name
            )
        except ValueError as e:
            logging.error("Token verification failed: %s", str(e))
            raise
        except Exception as e:
            logging.error("Unexpected error during token verification: %s", str(e))
            raise

    async def get_user(self, uid: str) -> User:
        try:
            logging.info("Attempting to get user with uid: %s", uid)
            user_info = auth.get_user(uid)
            logging.info("User info retrieved: %s", user_info)
            
            return User(
                uid=user_info.uid,
                email=user_info.email,
                display_name=user_info.display_name
            )
        except Exception as e:
            logging.error("User not found: %s", str(e))
            raise ValueError(f"User not found: {str(e)}")
