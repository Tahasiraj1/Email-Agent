import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from agents import function_tool

# Scopes: read-only Gmail inbox
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    creds = None

    # Use saved token if exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid creds, go through OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save the token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def list_latest_emails(service, max_results=1):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()

        for name, value in msg_data.items():
            if name == 'body':
                continue
            print(f"{name}: {value}")

        headers = msg_data.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(No Sender)")

        snippet = msg_data.get("snippet", "")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Snippet: {snippet}\n{'-'*50}")

        return (
            {
                "sender": sender,
                "subject": subject,
                "snippet": snippet
            }
        )

@function_tool
def list_emails():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    emails = list_latest_emails(service)
    return emails


if __name__ == '__main__':
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    result = list_latest_emails(service)
    print(result)
