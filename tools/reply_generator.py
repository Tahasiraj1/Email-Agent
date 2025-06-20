from .summarize import summarize_email
import google.generativeai as genai
from models.interfaces import Email
from email_modules.fetcher import EmailFetcher
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

def generate_email_content(email: Email = None, summary: str = None, user_query: str = None) -> str:
    """Generate an email draft, reply, or fully composed email based on context."""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

    # Compose the base prompt
    prompt = "You are a professional email assistant writing on behalf of Taha Siraj.\n"
    prompt += "NEVER add comments like 'Here's your reply' or 'Here's the draft'. Just output the email body.\n\n"
    prompt += "Never include spaces for my manual input or change, like this [Your Name] OR [Your Email] OR [Subject] OR [Body] OR [Attachments] OR [Hiring Manager Name] OR Anything like that.\n\n"

    if user_query:
        prompt += f"""📌 User Request:
        {user_query}

        ✉️ Compose an email that:
        - Addresses the recipient(s) mentioned or implied.
        - Includes Taha Siraj’s name if appropriate (e.g., closing).
        - Is natural, professional, clear, and concise.
        - Avoid unnecessary filler or extra politeness.
        """
    elif email and summary:
        
        prompt += f"""📌 Email Context:
        {email}

        📌 Summary:
        {summary}

        ✉️ Draft a reply that:
        - Answers the sender's query/request.
        - Includes Taha Siraj's name where appropriate.
        - Matches the sender's tone and style.
        - Is natural, professional, and free of filler or excessive politeness.
        """
    else:
        raise ValueError("Insufficient input: Provide either user_query or both email and summary.")
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Error generating email content: {e}")

if __name__ == "__main__":
    fether = EmailFetcher()
    email = fether.fetch_emails()
    print(email)
    summary = summarize_email(email)
    reply = generate_email_content(email=email, summary=summary)
    print(reply)