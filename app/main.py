"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.endpoints import extraction, health

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    Vision Studio - AI-Powered Data Extraction API
    
    Extract structured data from PDF and image files using state-of-the-art AI vision models.
    
    ## Features
    - **Multi-format support**: PDF, PNG, JPG, JPEG
    - **Dual AI models**: Google Gemini and Anthropic Claude
    - **Flexible extraction**: Reference-based or instruction-based
    - **Multi-page PDFs**: Automatic page processing and data aggregation
    
    ## Extraction Modes
    
    ### 1. Reference-Based Extraction
    Provide key-value pairs defining what to extract:
    ```json
    {
        "invoice_number": "Invoice #",
        "date": "Date",
        "total": "Total Amount"
    }
    ```
    
    ### 2. Instruction-Based Extraction
    Provide free-text instructions:
    ```
    "Extract all line items from this invoice including description, quantity, and price"
    ```
    
    ## Quick Start
    
    ```bash
    # Extract from PDF using reference values
    curl -X POST "http://localhost:8000/api/v1/extract" \\
      -F "file=@document.pdf" \\
      -F "ai_model=gemini" \\
      -F 'reference_values={"field1": "Label 1", "field2": "Label 2"}'
    
    # Extract using instructions
    curl -X POST "http://localhost:8000/api/v1/extract" \\
      -F "file=@image.jpg" \\
      -F "ai_model=claude" \\
      -F "instructions=Extract all visible text and organize by section"
    ```
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    extraction.router,
    prefix=settings.API_V1_PREFIX,
    tags=["extraction"]
)

app.include_router(
    health.router,
    prefix=settings.API_V1_PREFIX,
    tags=["health"]
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
