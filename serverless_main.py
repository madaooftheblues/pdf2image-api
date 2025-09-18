"""
Serverless version of the PDF2Image API using AWS Lambda
"""
import json
import base64
import tempfile
import zipfile
from io import BytesIO
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pdf2image import convert_from_bytes
from PIL import Image
from mangum import Mangum

app = FastAPI(
    title="PDF2Image API",
    description="Convert PDF files to images with high DPI support",
    version="1.0.0"
)

# Configuration
DEFAULT_DPI = 300
SUPPORTED_FORMATS = ["PNG", "JPEG", "JPG", "WEBP"]
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


@app.get("/")
async def root():
    return {
        "message": "PDF2Image API",
        "version": "1.0.0",
        "supported_formats": SUPPORTED_FORMATS,
        "default_dpi": DEFAULT_DPI
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/convert")
async def convert_pdf_to_images(
    file: UploadFile = File(...),
    format: str = "PNG",
    dpi: int = DEFAULT_DPI,
    quality: Optional[int] = None
):
    """
    Convert PDF to images.
    
    Args:
        file: PDF file to convert
        format: Output image format (PNG, JPEG, JPG, WEBP)
        dpi: DPI for image conversion (default: 300)
        quality: JPEG quality (1-100, only for JPEG format)
    
    Returns:
        Single image file or ZIP file containing multiple images
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Validate format
    format = format.upper()
    if format not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported format. Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )
    
    # Validate DPI
    if dpi < 72 or dpi > 600:
        raise HTTPException(status_code=400, detail="DPI must be between 72 and 600")
    
    # Validate quality for JPEG
    if format in ["JPEG", "JPG"] and quality is not None:
        if quality < 1 or quality > 100:
            raise HTTPException(status_code=400, detail="Quality must be between 1 and 100")
    
    try:
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large. Maximum size: 50MB")
        
        # Convert PDF to images
        images = convert_from_bytes(
            content,
            dpi=dpi,
            fmt=format.lower(),
            jpeg_quality=quality if format in ["JPEG", "JPG"] else None
        )
        
        if not images:
            raise HTTPException(status_code=400, detail="No pages found in PDF")
        
        # If single page, return the image directly
        if len(images) == 1:
            img_buffer = BytesIO()
            images[0].save(img_buffer, format=format)
            img_buffer.seek(0)
            
            return StreamingResponse(
                BytesIO(img_buffer.getvalue()),
                media_type=f"image/{format.lower()}",
                headers={
                    "Content-Disposition": f"attachment; filename=page_1.{format.lower()}"
                }
            )
        
        # Multiple pages - create ZIP file
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, image in enumerate(images, 1):
                img_buffer = BytesIO()
                image.save(img_buffer, format=format)
                img_buffer.seek(0)
                
                zip_file.writestr(
                    f"page_{i}.{format.lower()}",
                    img_buffer.getvalue()
                )
        
        zip_buffer.seek(0)
        
        return StreamingResponse(
            BytesIO(zip_buffer.getvalue()),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=pdf_images.zip"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


# AWS Lambda handler
handler = Mangum(app)
