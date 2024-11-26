from abc import ABC, abstractmethod
from app.domain.entities.text_generation import TextGenerationRequest, TextGenerationResponse

class TextGenerationRepository(ABC):
    @abstractmethod
    async def generate_text(self, request: TextGenerationRequest) -> TextGenerationResponse:
        """Generate text based on the input request"""
        pass
