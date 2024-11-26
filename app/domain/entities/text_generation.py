from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class TextGenerationRequest:
    inputs: str
    parameters: Optional[Dict[str, Any]] = None

@dataclass
class TextGenerationResponse:
    generated_text: str
    detected_language: str
