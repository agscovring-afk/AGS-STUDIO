from agents.architect import ArchitectAgent
from agents.database import DatabaseAgent
from agents.backend import BackendAgent
from agents.ui import UIAgent
from agents.testing import TestingAgent
from agents.documentation import DocumentationAgent


class AICodeGenerator:

    def __init__(self):

        self.architect = ArchitectAgent()
        self.database = DatabaseAgent()
        self.backend = BackendAgent()
        self.ui = UIAgent()
        self.testing = TestingAgent()
        self.documentation = DocumentationAgent()


    def generate(self,module):

        return {

            "architecture": self.architect.analyze(module),

            "database": self.database.analyze(module),

            "backend": self.backend.analyze(module),

            "ui": self.ui.analyze(module),

            "testing": self.testing.analyze(module),

            "documentation": self.documentation.analyze(module)

        }
