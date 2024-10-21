from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# CORS settings to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Request model for translation
class TranslationRequest(BaseModel):
    text: str
    source_language: Optional[str] = "auto"
    target_language: Optional[str] = "en"

# Endpoint to translate text
@app.post("/translate/")
async def translate(request: TranslationRequest):
    try:
        # Use GoogleTranslator from deep_translator to translate text
        translator = GoogleTranslator(source=request.source_language, target=request.target_language)
        translated_text = translator.translate(request.text)
        return {"translated_text": translated_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Translation failed: {str(e)}")

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Translation API"}

# Example usage:
# POST request to /translate/ with JSON body:
# {
#   "text": "Hello, how are you?",
#   "source_language": "en",
#   "target_language": "es"
# }
# Response:
# {
#   "translated_text": "Hola, ¿cómo estás?"
# }
