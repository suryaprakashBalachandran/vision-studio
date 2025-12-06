"""Data extraction endpoints."""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import json
from app.models import ExtractionResponse, AIModel, ModelInfo
from app.config import settings
from app.services import file_handler, extraction_service
from app.utils import validate_upload_file

router = APIRouter()


@router.post("/extract", response_model=ExtractionResponse)
async def extract_data(
    file: UploadFile = File(..., description="PDF or image file to extract data from"),
    ai_model: str = Form("gemini", description="AI model to use (default: 'gemini')"),
    reference_values: Optional[str] = Form(None, description="JSON string of key-value pairs for extraction"),
    instructions: Optional[str] = Form(None, description="Free-text instructions for extraction")
):
    """
    Extract data from uploaded file using Google Gemini AI vision model.
    
    **Request Parameters:**
    - **file**: PDF, PNG, JPG, or JPEG file (max 100MB)
    - **ai_model**: AI model to use (default: 'gemini', also supports 'claude' if configured)
    - **reference_values**: JSON string like '{"invoice_number": "Invoice #", "date": "Date"}'
    - **instructions**: Free-text instructions (used if reference_values not provided)
    
    **Response:**
    - **status**: 'success' or 'error'
    - **extracted_data**: Dictionary of extracted key-value pairs
    - **processing_time**: Time taken in seconds
    - **model_used**: AI model that was used
    - **pages_processed**: Number of pages/images processed
    
    **Example (using default Gemini model):**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/extract" \\
      -F "file=@invoice.pdf" \\
      -F 'reference_values={"invoice_number": "Invoice #", "total": "Total Amount"}'
    ```
    
    **Example (with explicit model selection):**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/extract" \\
      -F "file=@invoice.pdf" \\
      -F "ai_model=gemini" \\
      -F 'reference_values={"invoice_number": "Invoice #", "total": "Total Amount"}'
    ```
    """
    temp_file_path = None
    
    try:
        # Validate file
        await validate_upload_file(
            file,
            settings.allowed_extensions_list,
            settings.MAX_FILE_SIZE
        )
        
        # Validate AI model
        try:
            model_enum = AIModel(ai_model.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid AI model '{ai_model}'. Must be 'gemini' or 'claude'"
            )
        
        # Parse reference values if provided
        parsed_reference_values = None
        if reference_values:
            try:
                parsed_reference_values = json.loads(reference_values)
                if not isinstance(parsed_reference_values, dict):
                    raise ValueError("reference_values must be a JSON object")
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid JSON in reference_values: {str(e)}"
                )
        
        # Validate that at least one extraction mode is provided
        if not parsed_reference_values and not instructions:
            raise HTTPException(
                status_code=400,
                detail="Either 'reference_values' or 'instructions' must be provided"
            )
        
        # Save uploaded file
        temp_file_path, file_ext = await file_handler.save_upload_file(file)
        
        # Extract data
        result = await extraction_service.extract_from_file(
            file_path=temp_file_path,
            file_extension=file_ext,
            ai_model=model_enum,
            reference_values=parsed_reference_values,
            instructions=instructions
        )
        
        return ExtractionResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
    
    finally:
        # Cleanup temporary file
        if temp_file_path:
            file_handler.cleanup_file(temp_file_path)


@router.get("/models", response_model=list[ModelInfo])
async def get_available_models():
    """
    Get list of available AI models.
    
    Returns information about supported models and their availability.
    """
    models_available = extraction_service.check_model_availability()
    
    models = [
        ModelInfo(
            name="gemini",
            provider="Google",
            description="Google Gemini 1.5 Flash - Fast and efficient vision model",
            supports_vision=True
        ),
        ModelInfo(
            name="claude",
            provider="Anthropic",
            description="Claude 3 Sonnet - High-quality vision understanding",
            supports_vision=True
        )
    ]
    
    return models
