"""Pydantic models for API responses."""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class ExtractionResponse(BaseModel):
    """Response model for data extraction."""
    
    status: str = Field(
        ...,
        description="Status of the extraction (success or error)"
    )
    
    extracted_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extracted key-value pairs from the document"
    )
    
    confidence_scores: Optional[Dict[str, float]] = Field(
        None,
        description="Confidence scores for each extracted field (0.0 to 1.0)"
    )
    
    processing_time: float = Field(
        ...,
        description="Time taken to process the request in seconds"
    )
    
    model_used: str = Field(
        ...,
        description="AI model used for extraction"
    )
    
    pages_processed: int = Field(
        default=1,
        description="Number of pages/images processed"
    )
    
    error_message: Optional[str] = Field(
        None,
        description="Error message if status is 'error'"
    )


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str
    version: str
    models_available: Dict[str, bool]
