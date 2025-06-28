from agents import AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os

def get_gemini_model():
    load_dotenv()
    set_tracing_disabled(disabled=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    provider = AsyncOpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=api_key,
    )

    model = OpenAIChatCompletionsModel(
        openai_client=provider,
        model='gemini-2.5-flash-preview-05-20'
    )

    return model