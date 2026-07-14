from .domain_analyzer import DomainAnalyzer
from .task_strategy import TaskStrategy


class DynamicTaskEngine:

    def __init__(self):

        self.analyzer = DomainAnalyzer()
        self.strategy = TaskStrategy()


    def generate(self, request):

        domain = self.analyzer.analyze(request)

        return self.strategy.build(domain)
