"""Shared setup: load .env and build the chat model used by every lesson."""

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

MODEL = os.getenv("MODEL", "groq:openai/gpt-oss-120b")


def get_model(**kwargs):
    # init_chat_model picks the provider integration (langchain-groq here) from
    # the "provider:model" prefix, so swapping to OpenAI/Anthropic is one env var.
    return init_chat_model(MODEL, temperature=0, **kwargs)
