import aiofiles
from pathlib import Path
from src.orchestration.state import WorkflowState

class OutputBuilder:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    async def build(self, state: WorkflowState):
        if not state.case_study:
            return

        # Create platform directories
        platforms = ["linkedin", "instagram", "case_study"]
        for p in platforms:
            (self.output_dir / p).mkdir(parents=True, exist_ok=True)

        # Write files
        async with aiofiles.open(self.output_dir / "linkedin" / "post.txt", "w") as f:
            await f.write(state.linkedin_post or "")

        async with aiofiles.open(self.output_dir / "instagram" / "story_caption.txt", "w") as f:
            await f.write(state.instagram_caption or "")

        async with aiofiles.open(self.output_dir / "case_study" / "draft.txt", "w") as f:
            await f.write(state.case_study or "")

        async with aiofiles.open(self.output_dir / "qa_report.txt", "w") as f:
            await f.write(state.qa_report or "")

        print(f"--- Assets structured in {self.output_dir} ---")
