from googleapiclient.discovery import build
from email.mime.text import MIMEText
from services.auth import authenticate
import base64


class EmailReplier:
    def reply_to_email(self, email_id: str, reply_text: str) -> str:
        """Send a proper reply to an email using the original message metadata."""

        creds = authenticate()
        service = build('gmail', 'v1', credentials=creds)

        # Step 1: Get original message metadata
        original_msg = service.users().messages().get(
            userId='me', id=email_id, format='metadata').execute()
        headers = {h['name']: h['value']
                for h in original_msg['payload']['headers']}

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
