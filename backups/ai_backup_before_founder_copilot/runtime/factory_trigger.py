from app.ai.factory.factory_engine import factory


class FactoryTrigger:


    def build(self, request):

        return factory.build(request)


trigger = FactoryTrigger()
