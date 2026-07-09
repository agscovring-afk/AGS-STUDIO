from app.ai.providers.provider_manager import ProviderManager
from app.ai.plugins.initializer import plugin_initializer


class AutoFix:


    def __init__(self):

        plugin_initializer.initialize()

        self.ai = ProviderManager()



    def build_prompt(self, file, error):

        return f"""
You are AGS-STUDIO Auto Fix Engine.

Fix this Python file.

FILE:
{file}

ERROR:
{error}

Return only corrected Python code.
No markdown.
No explanation.
"""



    def fix(self,file,error):

        prompt = self.build_prompt(
            file,
            error
        )


        providers = self.ai.status()

        available = (
            providers
            .get("plugins", {})
        )


        if "ollama" not in available:

            return {
                "status":"failed",
                "reason":"Ollama plugin not loaded",
                "available":available
            }



        result = self.ai.chat(
            "ollama",
            prompt
        )


        if isinstance(result,dict):

            code = (
                result.get("response")
                or result.get("content")
                or ""
            )

        else:

            code = str(result)



        if code.strip():

            with open(
                file,
                "w",
                encoding="utf8"
            ) as f:

                f.write(code)


            return {
                "status":"fixed",
                "file":file
            }


        return {
            "status":"failed",
            "file":file
        }
