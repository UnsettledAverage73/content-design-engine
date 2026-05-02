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
        For videos, samples keyframes and returns the highest score.
        """
        from src.ingestion.video import extract_keyframes
        from src.config import SUPPORTED_VIDEO_EXTENSIONS
        
        if file_path.suffix.lower() in SUPPORTED_VIDEO_EXTENSIONS:
            keyframes = extract_keyframes(file_path)
            if not keyframes:
                return MediaScore(technical_score=1, marketing_score=1, justification="Failed to extract video keyframes.")
            
            best_score = None
            for timestamp, frame_data in keyframes:
                score = await self._get_vlm_score(frame_data)
                if best_score is None or score.marketing_score > best_score.marketing_score:
                    score.justification = f"[Frame at {timestamp:.2}s] {score.justification}"
                    best_score = score
            return best_score
        else:
            # Handle Image
            from PIL import Image
            import io
            
            with Image.open(file_path) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.thumbnail((1024, 1024))
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG', quality=85)
                image_data = img_byte_arr.getvalue()
            
            return await self._get_vlm_score(image_data)

    async def _get_vlm_score(self, image_data: bytes) -> MediaScore:
        prompt = """
        Evaluate this image/frame for a marketing content engine. 
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
