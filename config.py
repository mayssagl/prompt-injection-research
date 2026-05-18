from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Your 3 models
MODELS = {
    "llama3.3_70b": "llama-3.3-70b-versatile",
    "gemma2_9b": "gemma2-9b-it",
    "llama3.1_8b": "llama-3.1-8b-instant"
}

TEMPERATURE = 0.0  # never change this