from ags.ai.providers import ProviderManager
from ags.ai.fallback import FallbackEngine


class AIHub:


    def __init__(self):

        self.providers = ProviderManager()

        self.fallback = FallbackEngine()



    def ask(self, task):


        available = self.providers.get_available()


        return self.fallback.run(

            available,

            task

        )
