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
from src.config import OUTPUT_DIR

from src.database.client import SessionLocal
from src.database.models import Event as DBEvent, Asset as DBAsset, Generation as DBGeneration
from datetime import datetime

class ContentOrchestrator:
    def __init__(self):
        self.scorer = Scorer()
        self.logger = SelectionLogger(OUTPUT_DIR)
        self.analyst = AnalystAgent()
        self.creator = CreatorAgent()
        self.qa = QAAgent()

    async def run(self, input_dir: Path):
        print(f"--- Scanning directory: {input_dir} ---")
        files = await scan_directory(input_dir)
        print(f"Found {len(files)} media files.")

        state = WorkflowState()
        
        # Mocking event metadata for this demo
        state.event_metadata = {
            "event_name": "Tech Innovation Summit 2026",
            "location": "San Francisco",
            "date": "2026-05-02"
        }

        # DB Setup
        db = SessionLocal()
        db_event = DBEvent(
            name=state.event_metadata["event_name"],
            location=state.event_metadata["location"],
            date=datetime.fromisoformat(state.event_metadata["date"])
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)

        print("--- Evaluating and Selecting Media ---")
        for file_path in files:
            metadata = extract_metadata(file_path)
            score = await self.scorer.score_media(file_path)
            selected = is_selected(score)
            
            self.logger.log_evaluation(file_path, score, selected)
            
            # DB Persist Asset
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
        self.logger.save()
        print(f"Selected {len(state.selected_assets)} assets.")

        if not state.selected_assets:
            print("No assets met the quality threshold. Exiting.")
            db.close()
            return state

        print("--- Agent A (Analyst): Generating Case Study ---")
        state.case_study = await self.analyst.generate_case_study(state)
        db.add(DBGeneration(event_id=db_event.id, platform="case_study", content=state.case_study))

        print("--- Agent B (Social Creator): Generating Social Content ---")
        social_content = await self.creator.generate_social_content(state)
        state.linkedin_post = social_content["linkedin"]
        state.instagram_caption = social_content["instagram"]
        db.add(DBGeneration(event_id=db_event.id, platform="linkedin", content=state.linkedin_post))
        db.add(DBGeneration(event_id=db_event.id, platform="instagram", content=state.instagram_caption))

        print("--- Agent C (QA): Performing Self-Reflection ---")
        qa_result = await self.qa.verify_content(state)
        state.qa_report = qa_result["report"]
        state.is_verified = qa_result["is_verified"]
        
        # Update generation with QA report (simplification for this demo)
        db.commit() # Save generations first
        
        db.close()
        return state
