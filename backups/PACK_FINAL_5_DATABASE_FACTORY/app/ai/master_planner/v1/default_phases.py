from .models import BuildPhase, BuildTask
from .phase_registry import PhaseRegistry


registry = PhaseRegistry()


def register_default_phases():

    registry.clear()

    phases = [

        "phase10_ui_foundation_v2",

        "phase11_visual_designer_v1",

        "phase12_ai_app_builder_v1",

        "phase13_testing_platform_v1",

        "phase14_devops_platform_v1",

        "phase15_marketplace_v1",

        "phase16_cloud_platform_v1",

        "phase17_enterprise_platform_v1",

        "phase18_autonomous_company_v1",

        "phase19_production_hardening_v2",

        "phase20_final_release"

    ]

    for name in phases:

        phase = BuildPhase(name=name)

        phase.tasks.append(

            BuildTask(

                name=name,

                agent="architect"

            )

        )

        registry.register(phase)

    return registry
