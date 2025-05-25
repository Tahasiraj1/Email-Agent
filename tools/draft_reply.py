from tools.fetch_unread import fetch_emails
from tools.reply_generator import generate_reply
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from services.auth import authenticate
from models.interfaces import Email
import base64

def draft_email(email_id: str, draft_text: Email) -> str:
    """Draft an email."""

    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

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
    emails = fetch_emails()
    print(emails)

    reply = generate_reply(emails)
    print("\nReply: ", reply)
    # draft = draft_email(emails["email_id"], reply)
    # print("\nDraft: ", draft)

