import google.generativeai as genai
from agents import function_tool
import os
from tools.fetch_unread import list_emails

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

@function_tool
def summarize_email(email_content: str) -> str:
    """Summarize the content of a single email."""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    Summarize the following email:
    {email_content}
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    email = list_emails()

    print(f"\n{email}")
    summary = summarize_email(email)
    print("\nSummary: ", summary)