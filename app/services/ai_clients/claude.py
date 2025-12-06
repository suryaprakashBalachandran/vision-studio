"""Anthropic Claude Vision API client."""
import anthropic
from PIL import Image
from typing import List
from app.services.ai_clients.base import BaseAIClient
from app.services.image_processor import image_processor


class ClaudeClient(BaseAIClient):
    """Client for Anthropic Claude Vision API."""
    
    def __init__(self, api_key: str, model_name: str = "claude-3-sonnet-20240229"):
        """
        Initialize Claude client.
        
        Args:
            api_key: Anthropic API key
            model_name: Claude model name
        """
        super().__init__(api_key, model_name)
        self.validate_api_key()
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def _image_to_base64(self, image: Image.Image) -> str:
        """Convert image to base64 for Claude API."""
        processed_image = image_processor.process_for_ai(image)
        return image_processor.image_to_base64(processed_image, format="PNG")
    
    async def extract_from_image(
        self,
        image: Image.Image,
        prompt: str
    ) -> str:
        """
        Extract data from a single image using Claude.
        
        Args:
            image: PIL Image object
            prompt: Extraction prompt
        
        Returns:
            Raw response text from Claude
        """
        # Convert image to base64
        image_base64 = self._image_to_base64(image)
        
        # Create message with vision
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )
        
        return message.content[0].text
    
    async def extract_from_images(
        self,
        images: List[Image.Image],
        prompt: str
    ) -> str:
        """
        Extract data from multiple images using Claude.
        
        Args:
            images: List of PIL Image objects
            prompt: Extraction prompt
        
        Returns:
            Raw response text from Claude
        """
        if len(images) == 1:
            return await self.extract_from_image(images[0], prompt)
        
        # Build content array with all images
        content = []
        
        # Add all images first
        for idx, image in enumerate(images):
            image_base64 = self._image_to_base64(image)
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_base64,
                },
            })
        
        # Add prompt with multi-page context
        multi_page_prompt = f"""{prompt}

Note: This document has {len(images)} pages shown above. Analyze all pages and extract the requested information from across all pages. Combine the data into a single JSON response."""
        
        content.append({
            "type": "text",
            "text": multi_page_prompt
        })
        
        # Create message with multiple images
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
        )
        
        return message.content[0].text


def create_claude_client(api_key: str, model_name: str = "claude-3-sonnet-20240229") -> ClaudeClient:
    """
    Factory function to create Claude client.
    
    Args:
        api_key: Anthropic API key
        model_name: Claude model name
    
    Returns:
        Configured ClaudeClient instance
    """
    return ClaudeClient(api_key, model_name)
