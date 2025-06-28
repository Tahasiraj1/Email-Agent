from calendar_modules import get_calendar_events
from calendar_modules import create_calendar_event
from fastapi import FastAPI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/calendar")
async def get_events():
    try:
        logger.info("Fetching calendar events")
        events = get_calendar_events()
        return events
    except Exception as e:
        return {"error": str(e)}
    
@app.post('/create_event')
async def create_event(summary: str, description: str, start_datetime: str, end_datetime: str, attendees: list[dict]):
    try:
        logger.info("Creating calendar event")
        events = create_calendar_event(summary, description, start_datetime, end_datetime, attendees)
        return events
    except Exception as e:
        return {"error": str(e)}