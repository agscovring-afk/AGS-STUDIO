from app.ai.plugins.plugin_manager import plugin_manager


def load_default_providers():

    plugin_manager.register(
        "app.ai.plugins.providers.ollama_plugin",
        "OllamaPlugin"
    )


load_default_providers()
