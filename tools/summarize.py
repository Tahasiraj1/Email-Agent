import google.generativeai as genai
from models.interfaces import Email
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

def summarize_email(email_content: Email) -> str:
    """Summarize the content of a single email."""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    Summarize the following email:
    {email_content}
    """

    response = model.generate_content(prompt)
    return response.text