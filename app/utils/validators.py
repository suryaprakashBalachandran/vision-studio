"""Validation utilities for file uploads and requests."""
from fastapi import UploadFile, HTTPException
from typing import List
import os


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validate file extension.
    
    Args:
        filename: Name of the uploaded file
        allowed_extensions: List of allowed extensions (without dots)
    
    Returns:
        True if extension is valid
    
    Raises:
        HTTPException: If extension is not allowed
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    file_ext = filename.lower().split('.')[-1]
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type '.{file_ext}' not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    return True


def validate_file_size(file_size: int, max_size: int) -> bool:
    """
    Validate file size.
    
    Args:
        file_size: Size of the file in bytes
        max_size: Maximum allowed size in bytes
    
    Returns:
        True if size is valid
    
    Raises:
        HTTPException: If file is too large
    """
    if file_size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        file_size_mb = file_size / (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({file_size_mb:.2f}MB). Maximum size: {max_size_mb:.2f}MB"
        )
    
    return True


async def validate_upload_file(
    file: UploadFile,
    allowed_extensions: List[str],
    max_size: int
) -> bool:
    """
    Validate uploaded file.
    
    Args:
        file: FastAPI UploadFile object
        allowed_extensions: List of allowed extensions
        max_size: Maximum file size in bytes
    
    Returns:
        True if file is valid
    
    Raises:
        HTTPException: If validation fails
    """
    # Validate extension
    validate_file_extension(file.filename, allowed_extensions)
    
    # Read file to check size
    content = await file.read()
    file_size = len(content)
    
    # Reset file pointer
    await file.seek(0)
    
    # Validate size
    validate_file_size(file_size, max_size)
    
    return True
