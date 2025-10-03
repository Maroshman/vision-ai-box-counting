from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import base64
import json
import os
from PIL import Image
import io
from typing import Dict, Any, List
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Vision AI Box Counting API",
    description="AI-powered box counting and label extraction from images",
    version="1.0.0"
)

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise Exception("OPENAI_API_KEY must be set in .env file")

# Initialize OpenAI client (v2+ API)
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=openai_api_key)
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    raise Exception(f"Failed to initialize OpenAI client: {e}")

# For deployment - handle PORT environment variable
PORT = int(os.getenv("PORT", 8000))

# Pydantic models for request/response
class ImageBase64Request(BaseModel):
    image: str  # Base64 encoded image string

def encode_image_to_base64(image_bytes: bytes) -> str:
    """Convert image bytes to base64 string for OpenAI API"""
    return base64.b64encode(image_bytes).decode('utf-8')

def validate_image(file: UploadFile) -> bool:
    """Validate if uploaded file is a valid image"""
    allowed_types = [
        "image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif",
        "image/avif", "image/heic", "image/heif"  # Added more formats
    ]
    
    # Check content type
    if file.content_type and file.content_type.lower() in allowed_types:
        return True
    
    # Also check file extension as fallback
    if file.filename:
        filename_lower = file.filename.lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif', '.heic', '.heif']
        return any(filename_lower.endswith(ext) for ext in allowed_extensions)
    
    return False

def create_box_counting_prompt() -> str:
    """Create the AI prompt for box counting and label extraction"""
    try:
        # Read prompt from external file
        prompt_file = os.path.join(os.path.dirname(__file__), "prompt.txt")
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error("prompt.txt file not found, using fallback prompt")
        # Fallback prompt if file is missing
        return """
You are an expert computer vision AI specialized in counting boxes and extracting text labels from images.

Please analyze the provided image and count all visible boxes/packages/containers, extract any visible text labels, and identify box types.

Return your analysis in JSON format with total_count, box_details array, summary, and confidence_score.
"""
    except Exception as e:
        logger.error(f"Error reading prompt file: {e}")
        return "Count and analyze boxes in this image, return results in JSON format."

async def analyze_image_with_openai(image_base64: str) -> Dict[str, Any]:
    """Send image to OpenAI Vision API for box counting and label extraction"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",  # Latest vision model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": create_box_counting_prompt()
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000,
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        
        # Try to parse JSON from the response
        try:
            # First priority: Look for JSON content between ```json and ``` markdown blocks
            if '```json' in content:
                start_marker = content.find('```json') + 7
                end_marker = content.find('```', start_marker)
                if start_marker != -1 and end_marker != -1:
                    json_content = content[start_marker:end_marker].strip()
                    detected_boxes = json.loads(json_content)
                    return {"detected_boxes": detected_boxes}
            
            # Second priority: Look for JSON array (starts with [)
            array_start = content.find('[')
            array_end = content.rfind(']') + 1
            
            if array_start != -1 and array_end != -1:
                json_content = content[array_start:array_end]
                detected_boxes = json.loads(json_content)
                return {"detected_boxes": detected_boxes}
            
            # Third priority: Look for JSON object (starts with {)
            obj_start = content.find('{')
            obj_end = content.rfind('}') + 1
            if obj_start != -1 and obj_end != -1:
                json_content = content[obj_start:obj_end]
                parsed_obj = json.loads(json_content)
                return {"detected_boxes": parsed_obj}
            
            # If no JSON found, return empty array
            return {"detected_boxes": []}
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed: {e}, content: {content[:200]}...")
            # Final fallback: return empty array
            return {"detected_boxes": []}
            
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Vision AI Box Counting API",
        "version": "1.0.0",
        "endpoints": {
            "/count-boxes": "POST - Upload image file for box counting and label extraction",
            "/count-boxes-simple": "POST - Upload image file for simplified box counting",
            "/count-boxes-base64": "POST - Send base64 image for box counting and label extraction",
            "/health": "GET - Health check endpoint"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "box-counting-ai"}

@app.post("/count-boxes")
async def count_boxes(file: UploadFile = File(...)):
    """
    Count boxes and extract labels from uploaded image
    
    Args:
        file: Image file (JPEG, PNG, WebP, GIF)
        
    Returns:
        JSON response with box count and label information
    """
    try:
        # Log file info for debugging
        logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        # Validate file
        if not validate_image(file):
            logger.warning(f"File validation failed: {file.filename}, content_type: {file.content_type}")
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Supported: JPEG, PNG, WebP, GIF. Got: {file.content_type}"
            )
        
        # Check file size (limit to 20MB)
        file_bytes = await file.read()
        if len(file_bytes) > 20 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum size: 20MB")
        
        # Validate image can be opened
        try:
            # Test if we can open and process the image
            image = Image.open(io.BytesIO(file_bytes))
            
            # Convert AVIF/HEIC and other formats to RGB for compatibility
            if image.format in ['AVIF', 'HEIC', 'HEIF'] or image.mode not in ['RGB', 'RGBA']:
                logger.info(f"Converting image from {image.format}/{image.mode} to RGB")
                image = image.convert('RGB')
                
                # Save as JPEG in memory for processing
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='JPEG', quality=95)
                file_bytes = img_buffer.getvalue()
                logger.info(f"Converted image size: {len(file_bytes)} bytes")
            
            # Get basic info to verify it's valid
            image_format = image.format or "Converted"
            image_size = image.size
            logger.info(f"Image validated: format={image_format}, size={image_size}")
            
        except Exception as e:
            logger.error(f"Image validation failed: {str(e)}")
            # Try to give more helpful error message
            if "cannot identify image file" in str(e).lower():
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unsupported image format. Please use JPEG, PNG, WebP, or GIF. Detected file type may not be supported."
                )
            else:
                raise HTTPException(status_code=400, detail=f"Invalid or corrupted image file: {str(e)}")
        
        # Convert to base64 (no need to re-read since we already have file_bytes)
        image_base64 = encode_image_to_base64(file_bytes)
        
        # Analyze with OpenAI
        logger.info(f"Analyzing image: {file.filename}, size: {len(file_bytes)} bytes")
        result = await analyze_image_with_openai(image_base64)
        
        # Extract detected_boxes from the result and return in the new format
        detected_boxes = result.get("detected_boxes", [])
        
        # Add metadata
        response = {
            "filename": file.filename,
            "file_size_bytes": len(file_bytes),
            "detected_boxes": detected_boxes,
            "status": "success"
        }
        
        logger.info(f"Analysis completed for {file.filename}")
        return JSONResponse(content=response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/count-boxes-simple")
async def count_boxes_simple(file: UploadFile = File(...)):
    """
    Simplified box counting endpoint that returns just the count and labels
    
    Args:
        file: Image file (JPEG, PNG, WebP, GIF)
        
    Returns:
        Simplified JSON response with count and labels
    """
    try:
        # Use the main endpoint logic
        full_response = await count_boxes(file)
        
        # Extract simplified information - now using the new structure
        detected_boxes = full_response.get("detected_boxes", [])
        
        # Count total quantity and extract unique labels
        total_count = 0
        all_labels = []
        
        for box in detected_boxes:
            if isinstance(box, dict) and "quantity" in box:
                total_count += box.get("quantity", 0)
                label = box.get("label", "")
                if label and label != "unidentified":
                    all_labels.append(label)
        
        simple_response = {
            "count": total_count,
            "labels": list(set(all_labels)),  # Remove duplicates
            "detected_boxes": detected_boxes
        }
            
        return JSONResponse(content=simple_response)
        
    except Exception as e:
        logger.error(f"Simple endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/count-boxes-base64")
async def count_boxes_base64(request: ImageBase64Request):
    """
    Count boxes from base64 encoded image
    
    Args:
        request: JSON with base64 encoded image string
        
    Returns:
        JSON response with box count and label information
    """
    try:
        # Extract base64 string (handle data URL format)
        image_data = request.image
        if image_data.startswith('data:'):
            # Remove data URL prefix (e.g., "data:image/jpeg;base64,")
            image_data = image_data.split(',', 1)[1]
        
        # Decode base64 to bytes
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 image data: {str(e)}")
        
        # Validate and process image
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary and save as JPEG
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to bytes for processing
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=85)
            processed_image_bytes = img_byte_arr.getvalue()
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")
        
        # Check file size (20MB limit)
        if len(processed_image_bytes) > 20 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Image too large. Maximum size is 20MB.")
        
        logger.info(f"Processing base64 image: {len(processed_image_bytes)} bytes")
        
        # Convert to base64 for OpenAI API
        image_base64 = encode_image_to_base64(processed_image_bytes)
        
        # Analyze with OpenAI
        analysis_result = await analyze_image_with_openai(image_base64)
        
        # Extract detected_boxes from the analysis result and return in the new format
        detected_boxes = analysis_result.get("detected_boxes", [])
        
        return JSONResponse(content={
            "detected_boxes": detected_boxes,
            "image_info": {
                "size_bytes": len(processed_image_bytes),
                "format": "JPEG",
                "dimensions": f"{image.width}x{image.height}"
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Base64 endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
