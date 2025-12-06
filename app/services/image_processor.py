"""Image processing service."""
from PIL import Image
import base64
import io
from typing import List


class ImageProcessor:
    """Processes images for AI model consumption."""
    
    def __init__(self):
        # Maximum dimensions for AI APIs (adjust based on model limits)
        self.max_width = 2048
        self.max_height = 2048
        self.max_size_bytes = 20 * 1024 * 1024  # 20MB for most vision APIs
    
    def load_image(self, image_path: str) -> Image.Image:
        """
        Load image from file path.
        
        Args:
            image_path: Path to image file
        
        Returns:
            PIL Image object
        """
        return Image.open(image_path)
    
    def resize_if_needed(self, image: Image.Image) -> Image.Image:
        """
        Resize image if it exceeds maximum dimensions.
        
        Args:
            image: PIL Image object
        
        Returns:
            Resized image (or original if no resize needed)
        """
        width, height = image.size
        
        if width <= self.max_width and height <= self.max_height:
            return image
        
        # Calculate new dimensions maintaining aspect ratio
        ratio = min(self.max_width / width, self.max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def image_to_base64(self, image: Image.Image, format: str = "PNG") -> str:
        """
        Convert PIL Image to base64 string.
        
        Args:
            image: PIL Image object
            format: Image format (PNG, JPEG, etc.)
        
        Returns:
            Base64 encoded string
        """
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        img_bytes = buffered.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')
    
    def image_to_bytes(self, image: Image.Image, format: str = "PNG") -> bytes:
        """
        Convert PIL Image to bytes.
        
        Args:
            image: PIL Image object
            format: Image format (PNG, JPEG, etc.)
        
        Returns:
            Image bytes
        """
        buffered = io.BytesIO()
        
        # Convert RGBA to RGB if saving as JPEG
        if format.upper() == "JPEG" and image.mode == "RGBA":
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[3])
            rgb_image.save(buffered, format=format, quality=95)
        else:
            image.save(buffered, format=format)
        
        return buffered.getvalue()
    
    def process_for_ai(self, image: Image.Image) -> Image.Image:
        """
        Process image for AI model consumption.
        
        Args:
            image: PIL Image object
        
        Returns:
            Processed image ready for AI
        """
        # Resize if needed
        processed = self.resize_if_needed(image)
        
        # Convert to RGB if needed (some models don't support RGBA)
        if processed.mode not in ('RGB', 'L'):
            processed = processed.convert('RGB')
        
        return processed
    
    def process_images_batch(self, images: List[Image.Image]) -> List[Image.Image]:
        """
        Process multiple images.
        
        Args:
            images: List of PIL Image objects
        
        Returns:
            List of processed images
        """
        return [self.process_for_ai(img) for img in images]


# Global image processor instance
image_processor = ImageProcessor()
