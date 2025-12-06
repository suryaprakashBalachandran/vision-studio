"""Base class for AI vision clients."""
from abc import ABC, abstractmethod
from PIL import Image
from typing import Dict, Any, List


class BaseAIClient(ABC):
    """Abstract base class for AI vision clients."""
    
    def __init__(self, api_key: str, model_name: str):
        """
        Initialize AI client.
        
        Args:
            api_key: API key for the AI service
            model_name: Name of the model to use
        """
        self.api_key = api_key
        self.model_name = model_name
    
    @abstractmethod
    async def extract_from_image(
        self,
        image: Image.Image,
        prompt: str
    ) -> str:
        """
        Extract data from a single image using the AI model.
        
        Args:
            image: PIL Image object
            prompt: Extraction prompt
        
        Returns:
            Raw response text from the AI model
        """
        pass
    
    @abstractmethod
    async def extract_from_images(
        self,
        images: List[Image.Image],
        prompt: str
    ) -> str:
        """
        Extract data from multiple images using the AI model.
        
        Args:
            images: List of PIL Image objects
            prompt: Extraction prompt
        
        Returns:
            Raw response text from the AI model
        """
        pass
    
    def validate_api_key(self) -> bool:
        """
        Validate that API key is set.
        
        Returns:
            True if API key is valid
        
        Raises:
            ValueError: If API key is not set
        """
        if not self.api_key or self.api_key == "":
            raise ValueError(f"API key not configured for {self.__class__.__name__}")
        return True
