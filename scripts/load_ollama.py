import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # project root

from app.ai.plugins.plugin_manager import plugin_manager

plugin_manager.register(
    "ollama",
    "app.ai.plugins.providers.ollama_plugin",
    "OllamaPlugin"
)

print("OLLAMA REGISTERED")
