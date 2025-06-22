from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi.middleware.cors import CORSMiddleware
from utils.redis_collector import RedisCollector
from email_agents import email_assistant
from pydantic import BaseModel
from fastapi import FastAPI
import logging
from agents import Runner

scheduler = AsyncIOScheduler()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class Message(BaseModel):
    role: str
    content: str

async def run_agent(input_str: str = "Fetch latest emails from my inbox, and act accordingly."):
    result = await Runner.run(email_assistant, input=input_str)
    collector = RedisCollector()
    await collector.collect(result.final_output)
    return await collector.get_messages()

@app.post('/chat', response_model=Message)
async def chat(message: Message):
    logger.info(f"Received message: {message}")
    try:
        messages = await run_agent(message.content)
        return Message(role="AI", content=messages)
    except Exception as e:
        return Message(role="AI", content=f"❌ Internal error: {e}")

@app.get('/logs')
async def get_logs():
    try:
        collector = RedisCollector()
        messages = await collector.get_messages()
        return {'role': 'AI', 'content': messages}
    except Exception as e:
        return {'role': 'AI', 'content': f"❌ Internal error: {e}"}

async def scheduled_task():
    await run_agent()

scheduler.add_job(
    scheduled_task,
    trigger=IntervalTrigger(seconds=30),
    id="process_emails",
    name="Process Emails",
    replace_existing=True,
)

scheduler.start()
