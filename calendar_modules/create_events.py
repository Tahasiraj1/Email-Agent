from services.auth import authenticate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


@authenticate
def create_events(creds=None):
    """Create events in the user's calendar."""
    try:
        service = build('calendar', 'v3', credentials=creds)

        EVENT = {
            'summary': 'Meeting',
            'description': 'Discuss the latest project updates.',
            'start': {
                'dateTime': '2025-06-23T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2025-06-23T10:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'attendees': [
                {'email': 'tahasiraj200@gmail.com'},
            ],
        }

        event = service.events().insert(
            calendarId='primary',
            body=EVENT,
            sendNotifications=True,
        ).execute()

        print(event)
    except HttpError as e:
        raise Exception(f"Error creating event: {e}")


if __name__ == '__main__':
    create_events()