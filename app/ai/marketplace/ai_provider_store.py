class AIProviderStore:

    def list(self):

        return {
            "providers":
            [
                "OLLAMA",
                "OPENAI",
                "GEMINI",
                "CLAUDE"
            ],
            "status":"READY"
        }


store = AIProviderStore()
