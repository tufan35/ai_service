from app.domain.entities.text_generation import TextGenerationRequest, TextGenerationResponse
from app.domain.repositories.text_generation_repository import TextGenerationRepository

class GenerateTextUseCase:
    def __init__(self, text_generation_repository: TextGenerationRepository):
        self.text_generation_repository = text_generation_repository

    async def execute(self, request: TextGenerationRequest) -> TextGenerationResponse:
        return await self.text_generation_repository.generate_text(request)
