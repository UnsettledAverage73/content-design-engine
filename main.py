import asyncio
import sys
from pathlib import Path
from src.config import INPUT_DIR, OUTPUT_DIR
from src.orchestration.workflow import ContentOrchestrator
from src.output.builder import OutputBuilder

async def main():
    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
    else:
        input_path = INPUT_DIR

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
    asyncio.run(main())
