"""
app/ai/autonomous/final_check.py
"""

from __future__ import annotations

from .doctor import AutonomousDoctor
from .exporter import AutonomousExporter


def run_final_check(context):

    doctor = AutonomousDoctor(
        context
    )

    report = doctor.run()

    exporter = AutonomousExporter()

    exporter.export(
        report
    )

    return report