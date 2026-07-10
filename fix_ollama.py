from pathlib import Path

p = Path("app/ai/plugins/providers/ollama_plugin.py")

s = p.read_text(encoding="utf-8")

if 'name = "ollama"' not in s:
    s = s.replace(
        "class OllamaPlugin(AIProvider):",
        """class OllamaPlugin(AIProvider):

    name = "ollama"
    version = "1.0"
    capabilities = ["chat", "generation"]"""
    )

if "super().__init__()" not in s:
    s = s.replace(
        "def __init__(self):",
        """def __init__(self):
        super().__init__()"""
    )

p.write_text(s, encoding="utf-8")

print("Ollama plugin fixed")