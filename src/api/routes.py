from fastapi import APIRouter, HTTPException
from pathlib import Path
from src.api.models import ProcessEventRequest, ProcessEventResponse, MediaAssetResponse, BrandCreate, BrandResponse
from src.orchestration.workflow import ContentOrchestrator
from src.output.builder import OutputBuilder
from src.config import OUTPUT_DIR

from src.database.client import SessionLocal
from src.database.models import Event as DBEvent, Brand as DBBrand
from fastapi import APIRouter, HTTPException, Depends
from src.api.auth import get_current_user, User

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
            "asset_count": len(event.assets),
            "generation_count": len(event.generations)
        })
    db.close()
    return result

@router.post("/process-event", response_model=ProcessEventResponse)
async def process_event(request: ProcessEventRequest, user: User = Depends(get_current_user)):
    input_path = Path(request.input_path)
    if not input_path.exists():
        raise HTTPException(status_code=404, detail=f"Input path {request.input_path} not found")

    orchestrator = ContentOrchestrator()
    builder = OutputBuilder(OUTPUT_DIR)

    state = await orchestrator.run(input_path, brand_id=request.brand_id, user_id=user["id"])

    
    # Override metadata if provided
    if request.event_metadata:
        state.event_metadata.update(request.event_metadata)

    if not state or not state.selected_assets:
        return ProcessEventResponse(
            status="no_assets_selected",
            selected_assets=[],
            case_study=None,
            linkedin_post=None,
            instagram_caption=None,
            qa_report=None,
            dist_path=str(OUTPUT_DIR)
        )

    await builder.build(state)

    selected_assets = [
        MediaAssetResponse(
            file_path=asset.file_path,
            technical_score=asset.score["technical_score"],
            marketing_score=asset.score["marketing_score"],
            justification=asset.score["justification"]
        ) for asset in state.selected_assets
    ]

    return ProcessEventResponse(
        status="success",
        selected_assets=selected_assets,
        case_study=state.case_study,
        linkedin_post=state.linkedin_post,
        instagram_caption=state.instagram_caption,
        qa_report=state.qa_report,
        dist_path=str(OUTPUT_DIR)
    )
