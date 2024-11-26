from abc import ABC, abstractmethod
from app.domain.entities.auth import User, TokenVerification

class AuthRepository(ABC):
    @abstractmethod
    async def verify_token(self, token_verification: TokenVerification) -> User:
        """Verify the authentication token and return user information"""
        pass

    @abstractmethod
    async def get_user(self, uid: str) -> User:
        """Get user information by user ID"""
        pass
