from app.ai.autonomous_orchestrator.v1.engine import AutonomousOrchestratorEngine


class MockCore:

    def run(self, request):
        return {
            "status": "generated",
            "request": request
        }


def test_orchestrator():

    engine = AutonomousOrchestratorEngine(MockCore())

    result = engine.run("BUILD MODULE")

    assert result["state"] == "SUCCESS"
    assert result["result"]["status"] == "generated"
