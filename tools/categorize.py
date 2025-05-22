from agents import function_tool
from tools.fetch_unread import fetch_emails
import google.generativeai as genai
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

# @function_tool
def categorize_email() -> str:
    """Categorize an email based on its content."""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    emails_lst = []
    
    emails = fetch_emails()

    for email in emails:
        emails_lst.append(list(email))

    prompt = f"""
    Categorize the following email:
    {emails_lst}
    """

    response = model.generate_content(prompt)
    return response.text


if __name__ == '__main__':
    summary = categorize_email()
    print("\nSummary: ", summary)

    
