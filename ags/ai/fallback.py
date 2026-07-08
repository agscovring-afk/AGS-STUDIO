class FallbackEngine:

    def run(self, providers, task):

        last_error = None

        for provider in providers:

            try:

                print(f"[AI] Trying {provider.name}")

                result = provider.execute(task)

                print(f"[AI] Success {provider.name}")

                return result

            except Exception as error:

                last_error = error

                print(f"[AI] Failed {provider.name}: {error}")

                continue

        return {
            "status": "all providers failed",
            "error": str(last_error)
        }
