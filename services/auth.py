from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",  # Optional: to mark read/labels
    'https://www.googleapis.com/auth/calendar',
]

def authenticate(func):
    def wrapper(*args, **kwargs):
        creds=None
        # Use saved token if exists
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If no valid creds, go through OAuth
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080, prompt='consent', access_type='offline')

            # Save the token
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return func(*args, creds=creds, **kwargs)
    return wrapper