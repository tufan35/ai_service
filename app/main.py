from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.presentation.api.routes import router
from app.core.config import Settings
import uvicorn
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

security_scheme = {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Enter your Bearer token in the format: Bearer <token>"
}

app = FastAPI(
    title="AI Service API",
    description="""
    AI Service API provides text generation capabilities using various language models.
    
    ## Authentication
    All endpoints except `/verify-token` require Bearer token authentication.
    1. First, get a token using the `/verify-token` endpoint
    2. Use this token in the Authorization header for other endpoints
    
    ## Available Models
    - Mistral: A powerful language model for text generation
    - Mixtral: An advanced model with enhanced capabilities
    
    ## Text Generation Parameters
    - `max_new_tokens`: Maximum number of tokens to generate (default: 100)
    - `temperature`: Controls randomness (0.0-1.0, default: 0.7)
    """,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "authentication",
            "description": "Operations for user authentication"
        },
        {
            "name": "text-generation",
            "description": "Text generation using different AI models"
        }
    ]
)

# Add security scheme to OpenAPI
app.openapi_schema = None  # Reset OpenAPI schema
app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True,
    "clientId": "your-client-id"
}

# Load settings
settings = Settings()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Validate environment variables and initialize services
    settings.validate()
    logging.info("Application started successfully")

def start():
    """Launched with `python3 app/main.py`"""
    load_dotenv()  # Add this line to load .env file
    logging.info("Environment variables loaded")
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8083,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    start()
