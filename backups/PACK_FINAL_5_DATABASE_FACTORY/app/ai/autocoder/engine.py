from app.ai.providers.provider_manager import ProviderManager
from app.ai.parser.code_parser import CodeParser
from app.ai.autocoder.prompt_factory import PromptFactory


class AutoCoder:

    def __init__(self):

        self.ai = ProviderManager()
        self.parser = CodeParser()
        self.prompts = PromptFactory()


    def generate_python(self, prompt):

        result = self.ai.generate(prompt)

        if isinstance(result, dict):
            text = result.get("response", "")
        else:
            text = str(result)

        return self.parser.extract_python(text)


    def generate_sql(self, prompt):

        result = self.ai.generate(prompt)

        if isinstance(result, dict):
            text = result.get("response", "")
        else:
            text = str(result)

        return self.parser.extract_sql(text)
