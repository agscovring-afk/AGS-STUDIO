from app.ai.plugins.plugin_manager import plugin_manager

plugin_manager.register(
    "ollama",
    "app.ai.plugins.providers.ollama_plugin",
    "OllamaPlugin"
)

print("OLLAMA REGISTERED")
