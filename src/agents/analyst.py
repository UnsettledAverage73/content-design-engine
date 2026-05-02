from google import genai
from src.config import GEMINI_API_KEY
from src.orchestration.state import WorkflowState

class AnalystAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = "gemini-2.5-flash"

    async def generate_case_study(self, state: WorkflowState) -> str:
        prompt = f"""
        Generate a 300-word case study based on the following event media and metadata.
        Focus on the narrative, the impact of the event, and the quality of the moments captured.
        
        Selected Media Details:
        {state.selected_assets}
        
        Event Metadata:
        {state.event_metadata}
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text
