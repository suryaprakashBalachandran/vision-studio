"""PDF to image conversion service."""
import fitz  # PyMuPDF
from PIL import Image
import io
from typing import List
from app.config import settings


class PDFConverter:
    """Converts PDF files to images."""
    
    def __init__(self):
        self.max_pages = settings.MAX_PDF_PAGES
    
    def convert_pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """
        Convert PDF file to list of PIL Images.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            List of PIL Image objects, one per page
        
        Raises:
            ValueError: If PDF has too many pages
        """
        images = []
        
        # Open PDF
        pdf_document = fitz.open(pdf_path)
        
        # Check page count
        page_count = len(pdf_document)
        if page_count > self.max_pages:
            pdf_document.close()
            raise ValueError(
                f"PDF has {page_count} pages, maximum allowed is {self.max_pages}"
            )
        
        # Convert each page to image
        for page_num in range(page_count):
            page = pdf_document[page_num]
            
            # Render page to image (300 DPI for good quality)
            mat = fitz.Matrix(300/72, 300/72)  # 300 DPI
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            images.append(img)
        
        pdf_document.close()
        return images
    
    def get_page_count(self, pdf_path: str) -> int:
        """
        Get number of pages in PDF.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Number of pages
        """
        pdf_document = fitz.open(pdf_path)
        page_count = len(pdf_document)
        pdf_document.close()
        return page_count


# Global PDF converter instance
pdf_converter = PDFConverter()
