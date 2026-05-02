from google import genai
from src.config import GEMINI_API_KEY
from src.orchestration.state import WorkflowState

class QAAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = "gemini-2.5-flash"

    async def verify_content(self, state: WorkflowState) -> dict:
        prompt = f"""
        Perform a 'Self-Reflection' pass on the generated marketing content.
        Verify that all claims match the raw event facts and metadata provided.
        Prevent hallucinations. If something is incorrect, provide the corrected text.
        
        Event Facts: {state.event_metadata}
        Media Facts: {state.selected_assets}
        
        Generated Case Study: {state.case_study}
        Generated LinkedIn Post: {state.linkedin_post}
        Generated Instagram Caption: {state.instagram_caption}
        
        Respond with a report and indicate if the content is 'VERIFIED' or 'REQUIRES_FIX'.
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        
        # In a real scenario, we'd parse this more strictly.
        is_verified = "VERIFIED" in response.text.upper()
        return {
            "report": response.text,
            "is_verified": is_verified
        }
