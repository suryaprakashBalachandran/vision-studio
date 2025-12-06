"""Health check endpoints."""
from fastapi import APIRouter
from app.models import HealthResponse
from app.config import settings
from app.services import extraction_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns API status and available AI models.
    """
    models_available = extraction_service.check_model_availability()
    
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        models_available=models_available
    )
