from .instructions import COMPOSER_INSTRUCTIONS, EMAIL_ASSISTANT_INSTRUCTIONS, DRAFTER_INSTRUCTIONS
from tools.process_pipeline import process_emails_pipeline
from tools.compose_pipeline import compose_email_pipeline
from tools.draft_pipeline import draft_new_email_pipeline
from utils.gemini_model import get_gemini_model
from calendar_agents import calendar_agent
from agents import Agent, ModelSettings

model = get_gemini_model()

drafter_agent = Agent(
    name="Drafter Agent",
    instructions=DRAFTER_INSTRUCTIONS,
    model=model,
    tools=[draft_new_email_pipeline],
    model_settings=ModelSettings(tool_choice='draft_new_email_pipeline'),
)

composer_agent = Agent(
    name="Composer Agent",
    instructions=COMPOSER_INSTRUCTIONS,
    model=model,
    tools=[compose_email_pipeline],
    model_settings=ModelSettings(tool_choice='compose_email_pipeline'),
)

email_assistant = Agent(
    name="Email Assistant",
    instructions=EMAIL_ASSISTANT_INSTRUCTIONS,
    model=model,
    tools=[process_emails_pipeline],
    handoffs=[composer_agent, drafter_agent, calendar_agent],
)