from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ProcessEventRequest(BaseModel):
    input_path: Optional[str] = None # For local dev
    media_urls: Optional[List[str]] = None # For cloud SaaS
    brand_id: Optional[int] = None
    event_metadata: Optional[Dict[str, Any]] = None

class BrandCreate(BaseModel):
    name: str
    guidelines_pdf_path: Optional[str] = None

class BrandResponse(BaseModel):
    id: int
    name: str
    created_at: str

class MediaAssetResponse(BaseModel):
    file_path: str
    technical_score: int
    marketing_score: int
    justification: str

class ProcessEventResponse(BaseModel):
    status: str
    event_id: int
    message: str
