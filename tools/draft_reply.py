from agents import function_tool
import os
import google.generativeai as genai
from tools.fetch_unread import list_emails
from tools.summarize import summarize_email

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

# @function_tool
def draft_reply_to_email(email: str) -> str:
    """Draft a reply to an email."""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    summary = summarize_email(email)

    prompt = f"""
    Generate a draft reply to the following email:
    {email}
    
    Summary:
    {summary}
    """
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    email = list_emails()
    print(email['thread_id'])
    draft = draft_reply_to_email(email)
    print("\nDraft: ", draft)