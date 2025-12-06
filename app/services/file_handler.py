"""File handling service for uploads and temporary storage."""
from fastapi import UploadFile
import aiofiles
import os
import uuid
from typing import Tuple
from app.config import settings


class FileHandler:
    """Handles file uploads and temporary storage."""
    
    def __init__(self):
        self.temp_dir = settings.TEMP_DIR
        os.makedirs(self.temp_dir, exist_ok=True)
    
    async def save_upload_file(self, file: UploadFile) -> Tuple[str, str]:
        """
        Save uploaded file to temporary storage.
        
        Args:
            file: FastAPI UploadFile object
        
        Returns:
            Tuple of (file_path, file_extension)
        """
        # Generate unique filename
        file_ext = file.filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(self.temp_dir, unique_filename)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        return file_path, file_ext
    
    def cleanup_file(self, file_path: str) -> None:
        """
        Delete temporary file.
        
        Args:
            file_path: Path to file to delete
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")
    
    def cleanup_files(self, file_paths: list) -> None:
        """
        Delete multiple temporary files.
        
        Args:
            file_paths: List of file paths to delete
        """
        for file_path in file_paths:
            self.cleanup_file(file_path)
    
    def get_file_size(self, file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to file
        
        Returns:
            File size in bytes
        """
        return os.path.getsize(file_path)


# Global file handler instance
file_handler = FileHandler()
