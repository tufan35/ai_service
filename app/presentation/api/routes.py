from fastapi import APIRouter, HTTPException, Depends, Header, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.presentation.schemas.requests import TokenVerifyRequest, TextGenerationRequest
from app.presentation.schemas.responses import UserResponse, TextGenerationResponse
from app.domain.entities.auth import TokenVerification
from app.domain.entities.text_generation import TextGenerationRequest as DomainTextGenerationRequest
from app.domain.usecases.verify_auth import VerifyTokenUseCase, GetUserUseCase
from app.domain.usecases.generate_text import GenerateTextUseCase
from app.infrastructure.external.firebase_service import FirebaseService
from app.infrastructure.external.huggingface_service import HuggingFaceService
from typing import Annotated, Optional
import logging

router = APIRouter()
security = HTTPBearer()

# Dependencies
def get_auth_service():
    try:
        return FirebaseService()
    except Exception as e:
        logging.error("Error creating FirebaseService: %s", str(e))
        raise

def get_text_generation_service(model_name: str = "mistral"):
    return HuggingFaceService(model_name=model_name)

def get_verify_token_usecase(auth_service: Annotated[FirebaseService, Depends(get_auth_service)]):
    return VerifyTokenUseCase(auth_service)

def get_user_usecase(auth_service: Annotated[FirebaseService, Depends(get_auth_service)]):
    return GetUserUseCase(auth_service)

def get_text_generation_usecase(model_name: str):
    return GenerateTextUseCase(get_text_generation_service(model_name))

# Auth dependency
async def verify_token_header(
    credentials: HTTPAuthorizationCredentials = Security(security),
    usecase: VerifyTokenUseCase = Depends(get_verify_token_usecase)
):
    try:
        user = await usecase.execute(TokenVerification(id_token=credentials.credentials))
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logging.error("Error in verify_token_header: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="Internal server error during token verification",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/verify-token", response_model=UserResponse, tags=["authentication"])
async def verify_token(
    request: TokenVerifyRequest,
    usecase: Annotated[VerifyTokenUseCase, Depends(get_verify_token_usecase)]
):
    """
    Verify a Firebase ID token and return user information.
    
    This endpoint does not require authentication and is used to verify Firebase ID tokens.
    The token should be obtained from the Firebase Authentication client SDK.
    """
    try:
        logging.info("Verifying token...")
        user = await usecase.execute(TokenVerification(id_token=request.id_token))
        logging.info("Token verified successfully for user: %s", user.email)
        return UserResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name
        )
    except ValueError as e:
        logging.error("Token verification failed: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error("Unexpected error during token verification: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error during token verification")

@router.get("/user/{uid}", response_model=UserResponse, tags=["authentication"])
async def get_user(
    uid: str,
    user: Annotated[UserResponse, Security(security)],
    usecase: Annotated[GetUserUseCase, Depends(get_user_usecase)]
):
    """
    Get user information by UID.
    
    This endpoint requires authentication using a Bearer token.
    The UID should be a valid Firebase user ID.
    """
    try:
        user = await usecase.execute(uid)
        return UserResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model-specific endpoints
@router.post("/mistral", response_model=TextGenerationResponse, tags=["text-generation"])
async def generate_with_mistral(
    request: TextGenerationRequest,
    user: Annotated[UserResponse, Security(security)],
    usecase: Annotated[GenerateTextUseCase, Depends(lambda: get_text_generation_usecase("mistral"))]
):
    """
    Generate text using the Mistral model.
    
    This endpoint requires authentication using a Bearer token.
    You can control the generation using parameters like max_new_tokens and temperature.
    """
    try:
        domain_request = DomainTextGenerationRequest(
            inputs=request.inputs,
            parameters=request.parameters
        )
        result = await usecase.execute(domain_request)
        return TextGenerationResponse(
            generated_text=result.generated_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mixtral", response_model=TextGenerationResponse, tags=["text-generation"])
async def generate_with_mixtral(
    request: TextGenerationRequest,
    user: Annotated[UserResponse, Security(security)],
    usecase: Annotated[GenerateTextUseCase, Depends(lambda: get_text_generation_usecase("mixtral"))]
):
    """
    Generate text using the Mixtral model.
    
    This endpoint requires authentication using a Bearer token.
    You can control the generation using parameters like max_new_tokens and temperature.
    """
    try:
        domain_request = DomainTextGenerationRequest(
            inputs=request.inputs,
            parameters=request.parameters
        )
        result = await usecase.execute(domain_request)
        return TextGenerationResponse(
            generated_text=result.generated_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
