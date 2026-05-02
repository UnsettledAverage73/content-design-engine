import os
import asyncio
from pathlib import Path
from typing import Optional
from livekit.plugins import openai
from src.orchestration.state import WorkflowState

class VoiceAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            # Fallback or error handle. For now, we assume it's in .env
            pass

    async def generate_voice_over(self, text: str, output_path: Path) -> Optional[Path]:
        """
        Synthesizes text into speech and saves it as an MP3 file.
        """
        if not text:
            return None
            
        try:
            tts = openai.TTS(api_key=self.api_key, model="tts-1", voice="alloy")
            
            # Simple synthesis to file
            # LiveKit agents usually work in streams, but for this engine 
            # we want a static asset.
            
            audio_stream = tts.synthesize(text)
            
            # Write bytes to file
            with open(output_path, "wb") as f:
                async for audio_frame in audio_stream:
                    f.write(audio_frame.data)
            
            return output_path
        except Exception as e:
            print(f"Error generating voice-over: {e}")
            return None
