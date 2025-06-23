from calendar_modules.calendar_events import get_calendar_events
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