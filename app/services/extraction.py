"""Main extraction service orchestrator."""
from PIL import Image
from typing import Dict, Any, List, Optional
import time
from app.config import settings
from app.models import AIModel
from app.services.file_handler import file_handler
from app.services.pdf_converter import pdf_converter
from app.services.image_processor import image_processor
from app.services.ai_clients import create_gemini_client, create_claude_client
from app.utils import (
    build_reference_prompt,
    build_instruction_prompt,
    add_json_formatting_hint,
    parse_ai_response,
    validate_extracted_data
)


class ExtractionService:
    """Main service for orchestrating data extraction."""
    
    def __init__(self):
        self.gemini_client = None
        self.claude_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AI clients if API keys are available."""
        try:
            if settings.GEMINI_API_KEY:
                self.gemini_client = create_gemini_client(
                    settings.GEMINI_API_KEY,
                    settings.GEMINI_MODEL
                )
        except Exception as e:
            print(f"Failed to initialize Gemini client: {e}")
        
        try:
            if settings.CLAUDE_API_KEY:
                self.claude_client = create_claude_client(
                    settings.CLAUDE_API_KEY,
                    settings.CLAUDE_MODEL
                )
        except Exception as e:
            print(f"Failed to initialize Claude client: {e}")
    
    def _get_client(self, model: AIModel):
        """Get the appropriate AI client."""
        if model == AIModel.GEMINI:
            if not self.gemini_client:
                raise ValueError("Gemini API key not configured")
            return self.gemini_client
        elif model == AIModel.CLAUDE:
            if not self.claude_client:
                raise ValueError("Claude API key not configured")
            return self.claude_client
        else:
            raise ValueError(f"Unknown model: {model}")
    
    def _build_prompt(
        self,
        reference_values: Optional[Dict[str, str]],
        instructions: Optional[str]
    ) -> str:
        """Build extraction prompt based on mode."""
        if reference_values:
            prompt = build_reference_prompt(reference_values)
        elif instructions:
            prompt = build_instruction_prompt(instructions)
        else:
            raise ValueError("Either reference_values or instructions must be provided")
        
        # Add JSON formatting hints
        return add_json_formatting_hint(prompt)
    
    async def extract_from_file(
        self,
        file_path: str,
        file_extension: str,
        ai_model: AIModel,
        reference_values: Optional[Dict[str, str]] = None,
        instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract data from a file (PDF or image).
        
        Args:
            file_path: Path to the file
            file_extension: File extension (pdf, png, jpg, jpeg)
            ai_model: AI model to use
            reference_values: Optional key-value pairs for extraction
            instructions: Optional free-text instructions
        
        Returns:
            Dictionary with extraction results
        """
        start_time = time.time()
        images: List[Image.Image] = []
        
        try:
            # Convert file to images
            if file_extension == 'pdf':
                images = pdf_converter.convert_pdf_to_images(file_path)
            else:
                # Load image directly
                images = [image_processor.load_image(file_path)]
            
            # Build prompt
            prompt = self._build_prompt(reference_values, instructions)
            
            # Get AI client
            client = self._get_client(ai_model)
            
            # Extract data
            if len(images) == 1:
                response_text = await client.extract_from_image(images[0], prompt)
            else:
                response_text = await client.extract_from_images(images, prompt)
            
            # Parse response
            extracted_data = parse_ai_response(response_text)
            validated_data = validate_extracted_data(extracted_data)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            return {
                "status": "success",
                "extracted_data": validated_data,
                "processing_time": processing_time,
                "model_used": ai_model.value,
                "pages_processed": len(images),
                "error_message": None
            }
        
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                "status": "error",
                "extracted_data": {},
                "processing_time": processing_time,
                "model_used": ai_model.value,
                "pages_processed": len(images),
                "error_message": str(e)
            }
    
    def check_model_availability(self) -> Dict[str, bool]:
        """Check which AI models are available."""
        return {
            "gemini": self.gemini_client is not None,
            "claude": self.claude_client is not None
        }


# Global extraction service instance
extraction_service = ExtractionService()
