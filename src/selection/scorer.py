import json
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, MIN_TECHNICAL_SCORE, MIN_MARKETING_SCORE

class MediaScore(BaseModel):
    technical_score: int = Field(..., ge=1, le=10, description="Score for sharpness, exposure, and composition.")
    marketing_score: int = Field(..., ge=1, le=10, description="Score for brand presence, emotion, and hero shot potential.")
    justification: str = Field(..., description="Explanation for the assigned scores.")

class Scorer:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = "gemini-2.5-flash" # Use 2.5 flash for latest features and availability

    async def score_media(self, file_path: Path) -> MediaScore:
        """
        Scores a media file using Gemini VLM.
        """
        # Resize image to avoid SSL/Broken pipe issues with large files in this environment
        from PIL import Image
        import io
        
        with Image.open(file_path) as img:
            # Convert to RGB if necessary (e.g. for PNGs with alpha)
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Max dimension 1024px while preserving aspect ratio
            img.thumbnail((1024, 1024))
            
            # Save to byte stream
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=85)
            image_data = img_byte_arr.getvalue()

        prompt = """
        Evaluate this image for a marketing content engine. 
        Assign a technical_score (1-10) based on sharpness, exposure, and composition.
        Assign a marketing_score (1-10) based on brand logo visibility, human emotion, and 'hero shot' potential.
        Provide a brief justification for your scores.
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=[
                types.Part.from_bytes(data=image_data, mime_type="image/jpeg"),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MediaScore
            )
        )

        return MediaScore.model_validate_json(response.text)

def is_selected(score: MediaScore) -> bool:
    return score.technical_score >= MIN_TECHNICAL_SCORE and score.marketing_score >= MIN_MARKETING_SCORE
