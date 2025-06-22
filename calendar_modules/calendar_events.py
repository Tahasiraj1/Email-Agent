from services.auth import authenticate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime


@ authenticate
def get_calendar_events(creds=None):
    """Get events from the user's calendar."""
    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.now().isoformat() + 'Z'
        event_results = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime',
        ).execute()

        events = event_results.get('items', [])
        if not events:
            print("No upcoming events found.")
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    except HttpError as e:
        raise Exception(f"Error fetching calendar events: {str(e)}")


if __name__ == "__main__":
    get_calendar_events()