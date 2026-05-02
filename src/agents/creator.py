from google import genai
from src.config import GEMINI_API_KEY
from src.orchestration.state import WorkflowState

class CreatorAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = "gemini-2.5-flash"

    async def generate_social_content(self, state: WorkflowState) -> dict:
        brand_persona = state.brand_context or "You are a professional social media manager."
        
        linkedin_prompt = f"""
        {brand_persona}
        
        Write a professional LinkedIn post based on this event. 
        Focus on industry insights and networking value.
        
        Media Context: {state.selected_assets}
        Event Context: {state.event_metadata}
        """
        
        instagram_prompt = f"""
        {brand_persona}
        
        Write an energetic Instagram caption for a story or post.
        Use emojis and high-energy hooks.
        
        Media Context: {state.selected_assets}
        Event Context: {state.event_metadata}
        """
        
        linkedin_resp = self.client.models.generate_content(model=self.model_id, contents=linkedin_prompt)
        instagram_resp = self.client.models.generate_content(model=self.model_id, contents=instagram_prompt)
        
        return {
            "linkedin": linkedin_resp.text,
            "instagram": instagram_resp.text
        }
