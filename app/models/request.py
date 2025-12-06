"""Pydantic models for API requests."""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict
from enum import Enum


class AIModel(str, Enum):
    """Supported AI models for extraction."""
    GEMINI = "gemini"
    CLAUDE = "claude"


class ExtractionRequest(BaseModel):
    """Request model for data extraction."""
    
    ai_model: AIModel = Field(
        ...,
        description="AI model to use for extraction (gemini or claude)"
    )
    
    reference_values: Optional[Dict[str, str]] = Field(
        None,
        description="Key-value pairs defining fields to extract (e.g., {'invoice_number': 'Invoice #', 'date': 'Date'})"
    )
    
    instructions: Optional[str] = Field(
        None,
        description="Free-text instructions for extraction when reference_values is not provided"
    )
    
    @field_validator('reference_values', 'instructions')
    @classmethod
    def validate_extraction_mode(cls, v, info):
        """Ensure at least one extraction mode is provided."""
        # This will be called for both fields, so we check in the model_validator instead
        return v
    
    def model_post_init(self, __context):
        """Validate that at least one extraction mode is provided."""
        if not self.reference_values and not self.instructions:
            raise ValueError(
                "Either 'reference_values' or 'instructions' must be provided"
            )


class ModelInfo(BaseModel):
    """Information about an available AI model."""
    
    name: str
    provider: str
    description: str
    supports_vision: bool = True
