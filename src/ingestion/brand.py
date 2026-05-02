from pathlib import Path
from pypdf import PdfReader
from typing import Dict

def extract_brand_context(pdf_path: Path) -> str:
    """
    Extracts text from a brand guidelines PDF.
    """
    if not pdf_path.exists():
        return ""
    
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error parsing brand PDF: {e}")
        return ""

def get_brand_persona_prompt(brand_context: str) -> str:
    """
    Constructs a system prompt fragment based on brand context.
    """
    if not brand_context:
        return "You are a professional social media manager."
    
    # We could use Gemini to summarize the guidelines first, 
    # but for now we'll inject the raw text as context.
    return f"""
    You are an expert social media manager. You MUST follow these brand guidelines strictly:
    --- BRAND GUIDELINES START ---
    {brand_context}
    --- BRAND GUIDELINES END ---
    """
