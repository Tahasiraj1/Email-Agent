import google.generativeai as genai
from models.interfaces import Email
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

def generate_reply(email: Email, summary: str) -> str:
    """Generate a reply to an email."""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    My name is Taha Siraj. Mention my name in the email if needed.
    NEVER ADD extra lines such as 'Okay heres the reply for email...'
    Generate a reply to the following email:
    {email}
    
    Summary:
    {summary}
    """
    response = model.generate_content(prompt)
    return response.text