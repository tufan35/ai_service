from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    uid: str
    email: Optional[str] = None
    display_name: Optional[str] = None

class TextGenerationResponse(BaseModel):
    generated_text: str
    detected_language: Optional[str] = None
