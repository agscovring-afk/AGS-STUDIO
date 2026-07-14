from app.ai.autonomous_context.v1.engine import AutonomousContextEngine


def test_context_engine():

    engine = AutonomousContextEngine()

    result = engine.build("AGS-STUDIO")

    assert result["engine"] == "AUTONOMOUS_CONTEXT_ENGINE_V1"
    assert result["status"] == "completed"
    assert result["context"]["project"] == "AGS-STUDIO"
