import httpx
from typing import Dict, Any
import os
import asyncio
from app.domain.entities.text_generation import TextGenerationRequest, TextGenerationResponse
from app.domain.repositories.text_generation_repository import TextGenerationRepository
from app.core.language_detector import detect_language, format_prompt

class HuggingFaceService(TextGenerationRepository):
    MODELS = {
        "mistral": "mistralai/Mistral-7B-Instruct-v0.2",
        "mixtral": "mistralai/Mixtral-8x7B-Instruct-v0.1"
    }

    def __init__(self, model_name: str = "mistral"):
        if model_name not in self.MODELS:
            raise ValueError(f"Model {model_name} not supported. Available models: {', '.join(self.MODELS.keys())}")
            
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/models/{self.MODELS[model_name]}"
        self.token = os.getenv("HUGGINGFACE_TOKEN")
        if not self.token:
            raise ValueError("HUGGINGFACE_TOKEN environment variable is not set")

    async def generate_text(self, request: TextGenerationRequest) -> TextGenerationResponse:
        max_retries = 3
        retry_count = 0
        
        detected_lang = detect_language(request.inputs)
        formatted_prompt = format_prompt(request.inputs, detected_lang)

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        default_params = {
            "max_new_tokens": 1024,
            "temperature": 0.1,
            "top_p": 0.1,
            "do_sample": True,
            "return_full_text": False,
            "repetition_penalty": 1.2
        }

        payload = {
            "inputs": formatted_prompt,
            "parameters": request.parameters or default_params
        }

        while retry_count < max_retries:
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        self.api_url,
                        json=payload,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if isinstance(result, list) and len(result) > 0:
                            return TextGenerationResponse(
                                generated_text=result[0].get("generated_text", "").strip(),
                                detected_language=detected_lang
                            )
                    
                    if response.status_code == 503:
                        retry_count += 1
                        if retry_count < max_retries:
                            await asyncio.sleep(2)
                            continue
                    
                    response.raise_for_status()
                    
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise ValueError(f"Error calling Hugging Face API after {max_retries} attempts: {str(e)}")
                await asyncio.sleep(2)
                
        raise ValueError("Maximum retries reached")
