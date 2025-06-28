from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from services.auth import authenticate
from agents import function_tool


@function_tool
@authenticate
def create_calendar_event(
    summary: str,
    description: str,
    start_datetime: str,  # ISO format e.g. "2025-06-23T09:00:00-07:00"
    end_datetime: str,    # ISO format e.g. "2025-06-23T10:00:00-07:00"
    attendees: list[dict],
    timezone: str = "America/Los_Angeles",
    creds=None
):
    """
    Create a calendar event in the user's Google Calendar.

    Args:
    - summary: Title of the event.
    - description: Description of the event.
    - start_datetime: ISO8601 start time (e.g., "2025-06-23T09:00:00-07:00").
    - end_datetime: ISO8601 end time (e.g., "2025-06-23T10:00:00-07:00").
    - timezone: IANA timezone string (default is "America/Los_Angeles").
    - attendees: List of attendees as dicts, e.g., [{'email': 'name@example.com'}]

    returns:
    - status: A string indicating the success or failure of the operation.
    - htmlLink: The URL of the event in the user's calendar.
    - eventId: The ID of the created event.
    """
    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_datetime,
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": timezone,
            },
            "attendees": attendees,
        }

        created_event = service.events().insert(
            calendarId="primary",
            body=event,
            sendNotifications=True,
        ).execute()

        return {
            "status": "✅ Event created successfully.",
            "htmlLink": created_event.get("htmlLink"),
            "eventId": created_event.get("id")
        }

    except HttpError as e:
        raise Exception(f"❌ Error creating event: {e}")
