"""Configuration settings for Vision Studio."""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    GEMINI_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""
    
    # File Limits
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB in bytes
    MAX_PDF_PAGES: int = 50
    ALLOWED_EXTENSIONS: str = "pdf,png,jpg,jpeg"
    
    # Processing
    TEMP_DIR: str = "/tmp/vision-studio"
    
    # AI Models
    GEMINI_MODEL: str = "gemini-1.5-flash"
    CLAUDE_MODEL: str = "claude-3-sonnet-20240229"
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Vision Studio"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Get allowed extensions as a list."""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]


# Global settings instance
settings = Settings()

# Ensure temp directory exists
os.makedirs(settings.TEMP_DIR, exist_ok=True)
