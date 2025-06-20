from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from email_agents import email_assistant
from agents import Runner
from utils.message_collector import MessageCollector

# Configure loggingAdd commentMore actions
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

@app.post('/chat', response_model=Message)
async def chat(message: Message):
    logger.info(f"Received message: {message}")
    collector = MessageCollector()

    try:

        result = await Runner.run(email_assistant, input=message.content)
        collector.collect(result.final_output)

        messages = collector.get_messages()
        logger.info(f"Collected messages: {messages}")

        return Message(role="AI", content="\n".join(messages))
    except Exception as e:
        return Message(role="AI", content=f"❌ Internal error: {e}")