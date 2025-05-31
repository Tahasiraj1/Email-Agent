from email_agents.email_agent import email_assistant
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI
from agents import Runner
from typing import List

app = FastAPI()

origins = [
    "http://localhost:3000",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request body schema
class EmailRequest(BaseModel):
    user_input: str

@app.post("/emails")
async def process_emails(request: EmailRequest):
    result = await Runner.run(email_assistant, input=request.user_input)
    return {"status": "ok", "summary": result.final_output}