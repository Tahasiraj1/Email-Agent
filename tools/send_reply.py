from agents import function_tool
from tools.fetch_unread import list_emails, authenticate
from tools.draft_reply import draft_reply_to_email
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

def reply_to_email(service, email_id: str, reply_text: str) -> str:
    """Send a proper reply to an email using the original message metadata."""

    # Step 1: Get original message metadata
    original_msg = service.users().messages().get(userId='me', id=email_id, format='metadata').execute()
    headers = {h['name']: h['value'] for h in original_msg['payload']['headers']}

    to = headers.get('From')
    subject = headers.get('Subject', '(No Subject)')
    message_id = headers.get('Message-ID')
    thread_id = original_msg['threadId']

    # Step 2: Create MIME reply
    reply = MIMEText(reply_text)
    reply['To'] = to
    reply['Subject'] = f"Re: {subject}"
    reply['In-Reply-To'] = message_id
    reply['References'] = message_id

    # Step 3: Encode and send
    raw_message = base64.urlsafe_b64encode(reply.as_bytes()).decode()
    sent_msg = service.users().messages().send(
        userId='me',
        body={
            'raw': raw_message,
            'threadId': thread_id
        }
    ).execute()

    return sent_msg


if __name__ == '__main__':
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    email = list_emails()  # This should return dict with 'email_id' and 'thread_id'
    draft = draft_reply_to_email(email)

    reply = reply_to_email(service, email["email_id"], draft)
    print("\nReply: ", reply)
