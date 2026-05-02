import uuid
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from src.api.models import ProcessEventRequest, ProcessEventResponse, MediaAssetResponse, BrandCreate, BrandResponse
from src.api.auth import get_current_user, User
from src.orchestration.workflow import ContentOrchestrator
from src.output.builder import OutputBuilder
from src.config import OUTPUT_DIR
from src.database.client import SessionLocal
from src.database.models import Event as DBEvent, Brand as DBBrand
from src.ingestion.brand import extract_brand_context

router = APIRouter()

@router.post("/brands", response_model=BrandResponse)
async def create_brand(request: BrandCreate, user: User = Depends(get_current_user)):
    db = SessionLocal()
    brand_text = ""
    if request.guidelines_pdf_path:
        pdf_path = Path(request.guidelines_pdf_path)
        if pdf_path.exists():
            brand_text = extract_brand_context(pdf_path)

    db_brand = DBBrand(user_id=user["id"], name=request.name, guidelines_text=brand_text)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)

    response = BrandResponse(
        id=db_brand.id,
        name=db_brand.name,
        created_at=db_brand.created_at.isoformat()
    )
    db.close()
    return response

@router.get("/events")
async def list_events(user: User = Depends(get_current_user)):
    db = SessionLocal()
    events = db.query(DBEvent).filter(DBEvent.user_id == user["id"]).all()
    result = []
    for event in events:
        result.append({
            "id": event.id,
            "name": event.name,
            "location": event.location,
            "date": event.date,
            "status": event.status,
            "asset_count": len(event.assets),
            "generation_count": len(event.generations)
        })
    db.close()
    return result

@router.get("/events/{event_id}")
async def get_event(event_id: int, user: User = Depends(get_current_user)):
    db = SessionLocal()
    event = db.query(DBEvent).filter(DBEvent.id == event_id, DBEvent.user_id == user["id"]).first()
    if not event:
        db.close()
        raise HTTPException(status_code=404, detail="Event not found")
    
    result = {
        "id": event.id,
        "name": event.name,
        "location": event.location,
        "date": event.date,
        "status": event.status,
        "assets": [
            {
                "id": a.id,
                "file_path": a.file_path,
                "file_type": a.file_type,
                "technical_score": a.technical_score,
                "marketing_score": a.marketing_score,
                "justification": a.justification,
                "is_selected": a.is_selected
            } for a in event.assets
        ],
        "generations": [
            {
                "id": g.id,
                "platform": g.platform,
                "content": g.content,
                "qa_report": g.qa_report,
                "is_verified": g.is_verified
            } for g in event.generations
        ]
    }
    db.close()
    return result

@router.post("/process-event", response_model=ProcessEventResponse)
async def process_event(request: ProcessEventRequest, background_tasks: BackgroundTasks, user: User = Depends(get_current_user)):
    db = SessionLocal()
    
    # Create Event Record immediately
    event_name = request.event_metadata.get("event_name", "New Event") if request.event_metadata else "New Event"
    location = request.event_metadata.get("location", "Remote") if request.event_metadata else "Remote"
    
    db_event = DBEvent(
        user_id=user["id"],
        brand_id=request.brand_id,
        name=event_name,
        location=location,
        status="processing",
        job_id=str(uuid.uuid4())
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    orchestrator = ContentOrchestrator()
    
    # Launch in background
    background_tasks.add_task(
        orchestrator.run,
        event_id=db_event.id,
        input_dir=Path(request.input_path) if request.input_path else None,
        media_urls=request.media_urls,
        brand_id=request.brand_id,
        user_id=user["id"]
    )

    db.close()
    
    return ProcessEventResponse(
        status="processing",
        event_id=db_event.id,
        message="Event processing started in background."
    )
