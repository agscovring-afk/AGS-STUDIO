from app.ai.autonomous_core.v1.engine import AutonomousCoreEngine


def test_autonomous_core():

    engine = AutonomousCoreEngine()

    result = engine.run("BUILD ERP MODULE")

    assert result["engine"] == "AUTONOMOUS_REPORT_ENGINE_V1"
    assert result["status"] == "generated"
