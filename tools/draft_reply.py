from agents import function_tool
import os
import google.generativeai as genai
from tools.fetch_unread import fetch_emails
from tools.summarize import summarize_email
from email.mime.text import MIMEText
import base64
from googleapiclient.discovery import build
from services.auth import authenticate



gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

def generate_reply(email: str) -> str:
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


def draft_email(service, email_id: str, draft_text: str) -> str:
    """Draft an email."""

    email = service.users().messages().get(userId='me', id=email_id, format='metadata').execute()
    headers = {h['name']: h['value'] for h in email['payload']['headers']}

    to = headers.get('From')
    subject = headers.get('Subject', '(No Subject)')
    message_id = headers.get('Message-ID')
    thread_id = email['threadId']

    # Step 2: Create MIME reply
    draft = MIMEText(draft_text)
    draft['To'] = to
    draft['Subject'] = f"Re: {subject}"
    draft['In-Reply-To'] = message_id
    draft['References'] = message_id

    # Step 3: Encode and send
    raw_message = base64.urlsafe_b64encode(draft.as_bytes()).decode()

    # Call Gmail API to create draft
    draft_body = {
        'message': {
            'raw': raw_message
        }
    }

    draft = service.users().drafts().create(
        userId='me',
        body=draft_body
    ).execute()

    return draft


if __name__ == '__main__':
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    email = fetch_emails()
    reply = generate_reply(email)
    draft = draft_email(service, email["email_id"], reply)
    print("\nDraft: ", draft)