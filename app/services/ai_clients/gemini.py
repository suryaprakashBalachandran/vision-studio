"""Google Gemini Vision API client."""
import google.generativeai as genai
from PIL import Image
from typing import List
from app.services.ai_clients.base import BaseAIClient
from app.services.image_processor import image_processor


class GeminiClient(BaseAIClient):
    """Client for Google Gemini Vision API."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google AI API key
            model_name: Gemini model name
        """
        super().__init__(api_key, model_name)
        self.validate_api_key()
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    async def extract_from_image(
        self,
        image: Image.Image,
        prompt: str
    ) -> str:
        """
        Extract data from a single image using Gemini.
        
        Args:
            image: PIL Image object
            prompt: Extraction prompt
        
        Returns:
            Raw response text from Gemini
        """
        # Process image for AI
        processed_image = image_processor.process_for_ai(image)
        
        # Generate content with image and prompt
        response = self.model.generate_content([prompt, processed_image])
        
        return response.text
    
    async def extract_from_images(
        self,
        images: List[Image.Image],
        prompt: str
    ) -> str:
        """
        Extract data from multiple images using Gemini.
        
        For multi-page documents, we'll process each page and combine results.
        
        Args:
            images: List of PIL Image objects
            prompt: Extraction prompt
        
        Returns:
            Raw response text from Gemini
        """
        if len(images) == 1:
            return await self.extract_from_image(images[0], prompt)
        
        # Process all images
        processed_images = image_processor.process_images_batch(images)
        
        # Create multi-image prompt
        multi_page_prompt = f"""{prompt}

Note: This document has {len(images)} pages. Analyze all pages and extract the requested information from across all pages. Combine the data into a single JSON response."""
        
        # Build content list: [prompt, image1, image2, ...]
        content = [multi_page_prompt] + processed_images
        
        # Generate content with all images
        response = self.model.generate_content(content)
        
        return response.text


def create_gemini_client(api_key: str, model_name: str = "gemini-1.5-flash") -> GeminiClient:
    """
    Factory function to create Gemini client.
    
    Args:
        api_key: Google AI API key
        model_name: Gemini model name
    
    Returns:
        Configured GeminiClient instance
    """
    return GeminiClient(api_key, model_name)
