from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class MediaAsset(BaseModel):
    file_path: str
    metadata: Dict[str, Any]
    score: Dict[str, Any]

class WorkflowState(BaseModel):
    selected_assets: List[MediaAsset] = []
    event_metadata: Dict[str, Any] = {}
    case_study: Optional[str] = None
    linkedin_post: Optional[str] = None
    instagram_caption: Optional[str] = None
    qa_report: Optional[str] = None
    is_verified: bool = False
