from fastapi import APIRouter, HTTPException, status
from sentry_sdk import capture_exception, capture_message
from app.models import ImageAnalysisPayload,AdInsightsPayload
from app.llm_controllers.gemini_controller import analyze_image,get_ad_details

gemini_router = APIRouter()


@gemini_router.post('/analyze', status_code=status.HTTP_200_OK)
def queryVisionLLM(data: ImageAnalysisPayload):
    """
    Analyze an advertisement image using Gemini LLM.
    
    Args:
        data: ImageAnalysisPayload containing the image URL, optional brand ID, and optional custom prompt
        
    Returns:
        dict: Structured analysis of the image
    """
    try:
        result = analyze_image(
            image_url=data.image_url,
            prompt=data.prompt
        )
        capture_message("Image analysis completed successfully")
        return result
    except HTTPException as http_ex:
        capture_exception(http_ex)
        raise http_ex
    except Exception as e:
        capture_exception(e)
        raise HTTPException(status_code=500, detail=f"Failed to analyze image: {str(e)}")


@gemini_router.post('/get_ad_insights', status_code=status.HTTP_200_OK)
def get_ad_insights(data: AdInsightsPayload):
    """
    Get ad insights from an advertisement image using Gemini LLM.
    
    Args:
        data: ImageAnalysisPayload containing the image URL, optional brand ID, and optional custom prompt
        
    Returns:
        dict: Structured ad insights from the image
    """
    try:
        result = get_ad_details(
            image_url=data.image_url,
            brand_id=data.brand_id,
        )
        capture_message("Image analysis completed successfully")
        return result
    except HTTPException as http_ex:
        capture_exception(http_ex)
        raise http_ex
    except Exception as e:
        capture_exception(e)
        raise HTTPException(status_code=500, detail=f"Failed to analyze image: {str(e)}")
    
@gemini_router.get('/health', status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    return {
        "status": "healthy",
        "service": "Elendi-Service-API",
        "version": "1.0.0"
    }