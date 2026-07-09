from dotenv import load_dotenv
import os

load_dotenv()

MODELS = {
    "Gemini 2.5 Flash": "gemini/gemini-2.5-flash",
    "Gemini 2.5 Pro": "gemini/gemini-2.5-pro",

    "GPT-4.1 Mini": "openai/gpt-4.1-mini",
    "GPT-4.1": "openai/gpt-4.1",

    "Claude Haiku": "anthropic/claude-3-5-haiku-latest",
    "Claude Sonnet": "anthropic/claude-3-7-sonnet-latest",

    "Llama 3.3 (Groq)": "groq/llama-3.3-70b-versatile",
}


API_KEYS = {
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
}