from email_agents.instructions import COMPOSER_INSTRUCTIONS, EMAIL_ASSISTANT_INSTRUCTIONS, DRAFTER_INSTRUCTIONS
from agents import Agent, AsyncOpenAI, set_tracing_disabled, OpenAIChatCompletionsModel
from tools.process_pipeline import process_emails_pipeline
from tools.compose_pipeline import compose_email_pipeline
from tools.draft_pipeline import draft_new_email_pipeline
from tools.draft_pipeline import draft_new_email_pipeline
import os

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model='gemini-2.5-flash-preview-05-20',
    openai_client=provider,
)

drafter_agent = Agent(
    name="Drafter Agent",
    instructions=DRAFTER_INSTRUCTIONS,
    model=model,
    tools=[draft_new_email_pipeline],
)

composer_agent = Agent(
    name="Composer Agent",
    instructions=COMPOSER_INSTRUCTIONS,
    model=model,
    tools=[compose_email_pipeline],
)

email_assistant = Agent(
    name="Email Assistant",
    instructions=EMAIL_ASSISTANT_INSTRUCTIONS,
    model=model,
    tools=[process_emails_pipeline],
    handoffs=[composer_agent, drafter_agent],
)