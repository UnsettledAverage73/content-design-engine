import asyncio
from pathlib import Path
from typing import List
from src.ingestion.scanner import scan_directory
from src.ingestion.metadata import extract_metadata
from src.selection.scorer import Scorer, is_selected
from src.selection.logger import SelectionLogger
from src.orchestration.state import WorkflowState, MediaAsset
from src.agents.analyst import AnalystAgent
from src.agents.creator import CreatorAgent
from src.agents.qa import QAAgent
from src.agents.voice import VoiceAgent
from src.config import OUTPUT_DIR

from src.database.client import SessionLocal
from src.database.models import Event as DBEvent, Asset as DBAsset, Generation as DBGeneration
from datetime import datetime

from src.database.storage import StorageClient
import tempfile
import shutil

class ContentOrchestrator:
    def __init__(self):
        self.scorer = Scorer()
        self.logger = SelectionLogger(OUTPUT_DIR)
        self.analyst = AnalystAgent()
        self.creator = CreatorAgent()
        self.qa = QAAgent()
        self.voice = VoiceAgent()
        self.storage = StorageClient()

    async def run(self, event_id: int, input_dir: Optional[Path] = None, media_urls: Optional[List[str]] = None, brand_id: Optional[int] = None, user_id: Optional[str] = None):
        db = SessionLocal()
        db_event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
        if not db_event:
            print(f"Error: Event {event_id} not found.")
            return

        if not input_dir and not media_urls:
            db_event.status = "failed"
            db.commit()
            db.close()
            return

        # Workspace Setup
        temp_dir = Path(tempfile.mkdtemp())
        try:
            if media_urls:
                print(f"--- [Job {event_id}] Downloading media from cloud ---")
                files = []
                for i, url in enumerate(media_urls):
                    ext = ".jpg"
                    if ".mp4" in url.lower(): ext = ".mp4"
                    local_path = temp_dir / f"media_{i}{ext}"
                    if await self.storage.download_file(url, local_path):
                        files.append(local_path)
            else:
                files = await scan_directory(input_dir)
            
            state = WorkflowState()
            
            # Load Brand Context
            from src.database.models import Brand as DBBrand
            if brand_id:
                query = db.query(DBBrand).filter(DBBrand.id == brand_id)
                if user_id: query = query.filter(DBBrand.user_id == user_id)
                db_brand = query.first()
                if db_brand:
                    from src.ingestion.brand import get_brand_persona_prompt
                    state.brand_context = get_brand_persona_prompt(db_brand.guidelines_text)

            # Sync event metadata to state
            state.event_metadata = {
                "event_name": db_event.name,
                "location": db_event.location,
                "date": db_event.date.isoformat()
            }

            print(f"--- [Job {event_id}] Evaluating {len(files)} assets ---")
            for file_path in files:
                metadata = extract_metadata(file_path)
                score = await self.scorer.score_media(file_path)
                selected = is_selected(score)
                
                db_asset = DBAsset(
                    event_id=db_event.id,
                    file_path=str(file_path),
                    file_type="video" if file_path.suffix.lower() in [".mp4", ".mov"] else "image",
                    technical_score=score.technical_score,
                    marketing_score=score.marketing_score,
                    justification=score.justification,
                    metadata_json=metadata,
                    is_selected=selected
                )
                db.add(db_asset)

                if selected:
                    state.selected_assets.append(MediaAsset(
                        file_path=str(file_path),
                        metadata=metadata,
                        score=score.model_dump()
                    ))
            
            db.commit()

            if not state.selected_assets:
                db_event.status = "no_assets_selected"
                db.commit()
                db.close()
                return

            # Agents
            state.case_study = await self.analyst.generate_case_study(state)
            social_content = await self.creator.generate_social_content(state)
            state.linkedin_post = social_content["linkedin"]
            state.instagram_caption = social_content["instagram"]
            
            voice_path = temp_dir / "voice_over.mp3"
            generated_voice = await self.voice.generate_voice_over(state.instagram_caption, voice_path)
            
            if media_urls:
                remote_prefix = f"users/{user_id}/events/{db_event.id}"
                if generated_voice:
                    cloud_url = await self.storage.upload_file(voice_path, f"{remote_prefix}/instagram/voice_over.mp3")
                    db.add(DBGeneration(event_id=db_event.id, platform="instagram_voice", content=cloud_url))
                
                db.add(DBGeneration(event_id=db_event.id, platform="case_study", content=state.case_study))
                db.add(DBGeneration(event_id=db_event.id, platform="linkedin", content=state.linkedin_post))
                db.add(DBGeneration(event_id=db_event.id, platform="instagram", content=state.instagram_caption))
            else:
                db.add(DBGeneration(event_id=db_event.id, platform="case_study", content=state.case_study))
                db.add(DBGeneration(event_id=db_event.id, platform="linkedin", content=state.linkedin_post))
                db.add(DBGeneration(event_id=db_event.id, platform="instagram", content=state.instagram_caption))
                if generated_voice:
                    local_dest = OUTPUT_DIR / "instagram" / "voice_over.mp3"
                    local_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(voice_path, local_dest)
                    db.add(DBGeneration(event_id=db_event.id, platform="instagram_voice", content=str(local_dest)))

            db_event.status = "completed"
            db.commit()
            print(f"--- [Job {event_id}] Completed Successfully ---")
            
        except Exception as e:
            print(f"--- [Job {event_id}] Failed: {e} ---")
            db_event.status = "failed"
            db.commit()
        finally:
            shutil.rmtree(temp_dir)
            db.close()
