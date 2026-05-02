import asyncio
import sys
from pathlib import Path
from fastapi import FastAPI
import uvicorn
from src.api.routes import router
from src.config import INPUT_DIR, OUTPUT_DIR
from src.orchestration.workflow import ContentOrchestrator
from src.output.builder import OutputBuilder

app = FastAPI(title="Content Intelligence Engine API")
app.include_router(router, prefix="/api")

async def run_cli(input_path: Path):
    if not input_path.exists():
        print(f"Error: Input directory {input_path} does not exist.")
        return

    orchestrator = ContentOrchestrator()
    builder = OutputBuilder(OUTPUT_DIR)

    state = await orchestrator.run(input_path)
    
    if state and state.selected_assets:
        await builder.build(state)
        print("Content Intelligence Engine task completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else INPUT_DIR
        asyncio.run(run_cli(input_path))
