import json
import requests
import os
from PIL import Image
from io import BytesIO
from google import genai
from fastapi import HTTPException, status
from sentry_sdk import capture_exception
from dotenv import load_dotenv

load_dotenv()   

# Initialize Gemini API client
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_image(image_url: str, prompt: str):
    """
    Analyze an image using Gemini API and return structured analysis.
    
    Args:
        image_url: URL of the image to analyze
        prompt: Optional custom prompt for the image analysis
        
    Returns:
        dict: Structured analysis of the image
    """
    try:
        # Download the image from URL
        response = requests.get(image_url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to download image from URL: {image_url}"
            )
        
        # Open the image
        image = Image.open(BytesIO(response.content))

        # Generate response using Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, image]
        )

        # Extract response content
        response_text = response.text.strip()
        start = response_text.find("{")
        end = response_text.rfind("}")
        
        if start == -1 or end == -1:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to parse Gemini API response"
            )
            
        details = json.loads(response_text[start : end + 1])
                    
        return details
        
    except HTTPException as http_ex:
        capture_exception(http_ex)
        raise http_ex
    except Exception as e:
        capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze image: {str(e)}"
        ) 
    

def get_ad_details(image_url: str, brand_id: int = None):
    """
    Analyze an image using Gemini API and return structured analysis.
    
    Args:
        image_url: URL of the image to analyze
        brand_id: Optional brand ID associated with the image
        
    Returns:
        dict: Structured analysis of the image
    """
    try:
        # Download the image from URL
        response = requests.get(image_url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to download image from URL: {image_url}"
            )
        
        # Open the image
        image = Image.open(BytesIO(response.content))
        
        # Define the default prompt for image analysis
        default_prompt = (
            "Analyze this ad image for key marketing elements. Provide a structured JSON response with the following keys. "
            "Ensure each key is present in the JSON output. If a feature cannot be confidently identified, use 'None' as the value.\n\n"
            "Product Name: Extract only the **brand name and product type** (e.g., 'Himalaya Shampoo', 'Nike Shoes', 'Samsung TV'). Do not include extra details.\n"
            "Position of product: Provide the exact placement of the product (e.g., center, top-right, bottom-left, etc.).\n"
            "Position of logo: Provide the exact placement of the brand logo (e.g., top-left, top-right, center, etc.).\n"
            "Image Entities: Identify the key objects, people, or concepts visually present in the image (as a list of strings), ensuring that any line breaks (`\\n`) are replaced with spaces.\n"
            "Image Text Entities: Extract all discernible text from the image (as a list of strings), ensuring that any line breaks (`\\n`) are replaced with spaces.\n"
            "Offer in Adv: Extract the full price drop information in a clear format: 'Price slashed from ₹100 to ₹50'. Ensure that both the original and discounted prices are included with the correct currency symbol (₹). If a discount percentage (e.g., 'Flat 50% off') or special deals (e.g., 'Buy One Get One Free') are present, extract them fully and accurately. If no offer is present, state 'None'."
            "Performance Claim: If the ad makes any performance-related claims (e.g., 'Lasts 24 hours', 'Fastest delivery', '95% customer satisfaction'), extract the claim text. If none, use 'None'.\n"
            "Contrast in Adv: Assess the overall contrast in the ad (High, Medium, Low, None).\n"
            "Gender: Predict the primary target gender for this ad (Male, Female, Unisex, Not Applicable).\n"
            "Headline Size: Determine the approximate size of the main headline relative to other text (Small, Medium, Large, None).\n"
            "Subheadline Size: Determine the approximate size of the subheadline(s) relative to other text (Small, Medium, Large, None).\n"
            "CTA Button: If a call-to-action button is present, extract the text on it. If not, use 'None'.\n"
            "Engagement Prediction: Predict the likely level of user engagement with this ad (Likely, Neutral, Unlikely, None).\n"
            "Brand Keywords: Based on the visual and textual content, identify potential keywords associated with the brand or product (as a list of strings), ensuring that any line breaks (`\\n`) are replaced with spaces.\n"
            "Overall Sentiment: Describe the overall feeling or emotion conveyed by the ad (e.g., positive, neutral, exciting, informative, None).\n"
            "Key Message: Summarize the main message the ad is trying to communicate in one concise sentence (or 'None' if unclear).\n"
            "Recommendation: Deliver a precise, impactful recommendation to boost brand growth, customer engagement, and preference."
        )
        
        # Generate response using Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[default_prompt, image]
        )

        # Extract response content
        response_text = response.text.strip()
        start = response_text.find("{")
        end = response_text.rfind("}")
        
        if start == -1 or end == -1:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to parse Gemini API response"
            )
            
        details = json.loads(response_text[start : end + 1])
        
        # Add brand_id to the response if provided
        if brand_id:
            details["brand_id"] = brand_id
            
        return details
        
    except HTTPException as http_ex:
        capture_exception(http_ex)
        raise http_ex
    except Exception as e:
        capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze image: {str(e)}"
        ) 