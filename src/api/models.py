from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ProcessEventRequest(BaseModel):
    input_path: str
    event_metadata: Optional[Dict[str, Any]] = None

class MediaAssetResponse(BaseModel):
    file_path: str
    technical_score: int
    marketing_score: int
    justification: str

class ProcessEventResponse(BaseModel):
    status: str
    selected_assets: List[MediaAssetResponse]
    case_study: Optional[str]
    linkedin_post: Optional[str]
    instagram_caption: Optional[str]
    qa_report: Optional[str]
    dist_path: str
