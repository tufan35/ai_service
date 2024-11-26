from pydantic import BaseModel
from typing import Optional, Dict, Any

class TokenVerifyRequest(BaseModel):
    id_token: str

class TextGenerationRequest(BaseModel):
    inputs: str
    parameters: Optional[Dict[str, Any]] = None
