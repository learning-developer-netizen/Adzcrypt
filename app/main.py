from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import geminiLLM
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Service-API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      #["https://your-frontend-domain.com"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(geminiLLM.gemini_router, prefix="/api/gemini", tags=["Gemini LLM Image Analysis"])

@app.get("/")
async def root():
    return {"message": "Navigate to /docs for API documentation."} 