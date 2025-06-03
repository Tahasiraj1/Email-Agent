from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from services.auth import authenticate
from email.message import EmailMessage
import mimetypes
import base64

class EmailComposer:
    @authenticate
    def compose_email(self, to: str, subject: str, body: str, creds=None, attachments: list = None) -> str:
        """Compose an email."""
        try:
            service = build('gmail', 'v1', credentials=creds)
            profile = service.users().getProfile(userId='me').execute()

            # Step 1: Create MIME reply
            email = EmailMessage()
            email['To'] = to
            email['from'] = profile['emailAddress']
            email['Subject'] = subject
            email.set_content(body)

            # attachment
            if attachments:
                for attachment in attachments:
                    # guessing the MIME type
                    type_subtype, _ = mimetypes.guess_type(attachment)
                    maintype, subtype = type_subtype.split("/")

                    with open(attachment, "rb") as fp:
                        attachment_data = fp.read()
                    email.add_attachment(attachment_data, maintype, subtype)
            else:
                print(f"\n\n\nNo attachments found.\n\n\n")


            # Step 2: Encode and send
            raw_message = base64.urlsafe_b64encode(email.as_bytes()).decode()

            sent_msg = service.users().messages().send(
                userId='me',
                body={
                    'raw': raw_message
                }
            ).execute()

            return sent_msg
        except HttpError as e:
            raise Exception(f"Error sending email: {e}")