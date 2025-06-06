from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from email.message import EmailMessage
from services.auth import authenticate
from dataclasses import dataclass
from typing import Optional, List
import mimetypes


@dataclass
class ReplyDraftEmailBuilder:
    email_id: str
    reply_text: str

    @authenticate
    def structure(self, creds=None):
        """Structure the reply text for a given email."""
        try:
            service = build('gmail', 'v1', credentials=creds)

            # Step 1: Get original message metadata
            original_msg = service.users().messages().get(userId='me', id=self.email_id, format='metadata').execute()
            headers = {h['name']: h['value'] for h in original_msg['payload']['headers']}
            
            to = headers.get('From')
            subject = headers.get('Subject', '(No Subject)')
            message_id = headers.get('Message-ID')
            thread_id = original_msg['threadId']

            # Step 2: Create MIME reply
            reply = EmailMessage()
            reply['To'] = to
            reply['Subject'] = f"Re: {subject}"
            reply['In-Reply-To'] = message_id
            reply['References'] = message_id
            reply.set_content(self.reply_text)

            return reply, service, thread_id
        except HttpError as e:
            raise Exception(f"Error Structure Reply: {e}")



@dataclass
class NewEmailBuilder:
    to: str
    subject: str
    reply_text: str
    attachments: Optional[List[str]] = None
        
    @authenticate
    def structure(self, creds=None):
        """Structure the reply text for a given email."""
        try:
            service = build('gmail', 'v1', credentials=creds)
            profile = service.users().getProfile(userId='me').execute()

            # Step 1: Create MIME reply
            email = EmailMessage()
            email['To'] = self.to
            email['from'] = profile['emailAddress']
            email['Subject'] = self.subject
            email.set_content(self.reply_text)

            # attachment
            if self.attachments:
                for attachment in self.attachments:
                    # guessing the MIME type
                    type_subtype, _ = mimetypes.guess_type(attachment)
                    maintype, subtype = type_subtype.split("/")

                    with open(attachment, "rb") as fp:
                        attachment_data = fp.read()
                    email.add_attachment(attachment_data, maintype, subtype)
            else:
                pass
            return email, service
        except HttpError as e:
            raise Exception(f"Error Structure Email: {e}")