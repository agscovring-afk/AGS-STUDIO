from .models import ProjectContext
from .scanner import ProjectScanner
from .dependency import DependencyAnalyzer


class AutonomousContextEngine:

    def __init__(self):

        self.scanner = ProjectScanner()
        self.dependency = DependencyAnalyzer()


    def build(self, project):

        context = ProjectContext(project)

        scan = self.scanner.scan(project)

        context.set_metadata(
            "scan",
            scan
        )

        deps = self.dependency.analyze(context)

        context.set_metadata(
            "dependencies",
            deps
        )

        return {
            "engine": "AUTONOMOUS_CONTEXT_ENGINE_V1",
            "status": "completed",
            "context": context.export()
        }
