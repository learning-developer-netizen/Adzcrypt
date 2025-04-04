from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class AdInsightsPayload(BaseModel):
    """
    A class to represent the payload for the GeminiLLM ad insights endpoint.
    """
    image_url: str = Field(
        ..., 
        example="https://c8.alamy.com/comp/W63879/hot-sauce-product-ads-with-chili-peppers-in-fire-shape-3d-illustration-W63879.jpg",
        prompt="URL of the image to analyze"
    )
    brand_id: Optional[int] = Field(
        None,           
        example=1,
        description="Optional brand ID associated with the image"
    )
    
    class Config:   
        json_schema_extra = {
            "example": {
                "image_url": "https://c8.alamy.com/comp/W63879/hot-sauce-product-ads-with-chili-peppers-in-fire-shape-3d-illustration-W63879.jpg",
                "brand_id": 1
            }
        }

class ImageAnalysisPayload(BaseModel):
    """
    A class to represent the payload for the GeminiLLM image analysis endpoint.
    """
    image_url: str = Field(
        ..., 
        example="https://firebasestorage.googleapis.com/v0/b/brand-management-2logld.appspot.com/o/generated-images%2F1%2Ffashion_studio_images%2F1742733413718-esuhal.jpg?alt=media&token=238331b8-e4fa-46a9-b45a-d2242992fbd0",
        prompt="URL of the image to analyze"
    )
    brand_id: Optional[int] = Field(
        None, 
        example=1, 
        description="Optional brand ID associated with the image"
    )
    prompt: Optional[str] = Field(
        None,
        example="Analyze this advertisement image and provide insights about the marketing strategy.",
        description="Optional custom prompt for the image analysis. If not provided, a default marketing analysis prompt will be used."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "https://firebasestorage.googleapis.com/v0/b/brand-management-2logld.appspot.com/o/generated-images%2F1%2Ffashion_studio_images%2F1742733413718-esuhal.jpg?alt=media&token=238331b8-e4fa-46a9-b45a-d2242992fbd0",
                "prompt": "Analyze this advertisement image and provide insights about the marketing strategy."
            }
        } 