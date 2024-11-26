from app.domain.entities.auth import User, TokenVerification
from app.domain.repositories.auth_repository import AuthRepository

class VerifyTokenUseCase:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    async def execute(self, token_verification: TokenVerification) -> User:
        return await self.auth_repository.verify_token(token_verification)

class GetUserUseCase:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    async def execute(self, uid: str) -> User:
        return await self.auth_repository.get_user(uid)
