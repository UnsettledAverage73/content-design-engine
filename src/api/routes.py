from fastapi import APIRouter, HTTPException
from pathlib import Path
from src.api.models import ProcessEventRequest, ProcessEventResponse, MediaAssetResponse
from src.orchestration.workflow import ContentOrchestrator
from src.output.builder import OutputBuilder
from src.config import OUTPUT_DIR

router = APIRouter()

@router.post("/process-event", response_model=ProcessEventResponse)
async def process_event(request: ProcessEventRequest):
    input_path = Path(request.input_path)
    if not input_path.exists():
        raise HTTPException(status_code=404, detail=f"Input path {request.input_path} not found")

    orchestrator = ContentOrchestrator()
    builder = OutputBuilder(OUTPUT_DIR)

    state = await orchestrator.run(input_path)
    
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
