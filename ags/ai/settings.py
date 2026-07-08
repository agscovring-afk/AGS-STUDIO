import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama")
AI_MODEL = os.getenv("AI_MODEL", "qwen2.5:3b")
AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "180"))
AI_MODE = os.getenv("AI_MODE", "fast")
PIPELINE_VERSION = int(os.getenv("PIPELINE_VERSION", "2"))
