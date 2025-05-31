from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from email_agents.email_agent import email_assistant
from pydantic import BaseModel
from fastapi import FastAPI
from agents import Runner
import asyncio

app = FastAPI()

scheduler = BackgroundScheduler()

# Reusable agent runner function
async def run_email_agent(user_input: str):
    result = await Runner.run(email_assistant, input=user_input)
    return result.final_output

@app.post("/emails")
async def process_emails(email: BaseModel):
    # Call agent with dynamic input from the POST body
    summary = await run_email_agent(email.user_input)
    return {"status": "ok", "summary": summary}

def scheduled_task():
    asyncio.run(run_email_agent("Send an email to tahasiraj200@gmail.com, about the latest feature I added in my Email Agent Project, i.e APScheduler."))

scheduler.add_job(
    scheduled_task,
    trigger=IntervalTrigger(seconds=30),
    id="process_emails",
    name="Process Emails",
    replace_existing=True,
)

scheduler.start()