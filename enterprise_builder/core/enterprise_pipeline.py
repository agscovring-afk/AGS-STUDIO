from enterprise_builder.core.enterprise_generator import EnterpriseGenerator
from enterprise_builder.core.enterprise_manifest import EnterpriseManifest
from enterprise_builder.core.enterprise_registry import EnterpriseRegistry
from enterprise_builder.core.enterprise_config import EnterpriseConfig
from enterprise_builder.core.module_discovery import ModuleDiscovery
from enterprise_builder.core.tenant_foundation import TenantFoundation
from enterprise_builder.generators.workspace_generator import WorkspaceGenerator
from enterprise_builder.pipeline.release_builder import ReleaseBuilder

from enterprise_builder.core.enterprise_validator import EnterpriseValidator
from enterprise_builder.core.enterprise_report import EnterpriseReport
from enterprise_builder.core.release_report import ReleaseReport

from enterprise_builder.runtime import (
    RuntimeManager,
    StateManager,
    ExecutionContext,
    ExecutionGraph,
)


class EnterprisePipeline:

    def __init__(self):

        self.generator = EnterpriseGenerator()
        self.manifest = EnterpriseManifest()
        self.registry = EnterpriseRegistry()
        self.config = EnterpriseConfig()
        self.discovery = ModuleDiscovery()
        self.tenant = TenantFoundation()
        self.workspace = WorkspaceGenerator()
        self.release = ReleaseBuilder()

        self.validator = EnterpriseValidator()
        self.report = EnterpriseReport()
        self.release_report = ReleaseReport()

        self.runtime = RuntimeManager()
        self.state = StateManager()
        self.context = ExecutionContext()
        self.graph = ExecutionGraph()


    def execute(self, name="AGS_ENTERPRISE"):

        self.runtime.start()

        for step in (
            "generator",
            "config",
            "modules",
            "workspace",
            "tenant",
            "manifest",
            "registry",
            "release",
            "validation",
            "report",
        ):
            self.graph.add(step)


        output = {}

        output["generator"] = self.generator.create()
        output["config"] = self.config.load()
        output["modules"] = self.discovery.discover()
        output["workspace"] = self.workspace.generate()
        output["tenant"] = self.tenant.create()

        output["manifest"] = self.manifest.generate(name)

        self.registry.register(
            name,
            output["manifest"]
        )

        output["release"] = self.release.build()

        output["validation"] = self.validator.validate()


        report_data = {
            "generator": output["generator"],
            "config": output["config"],
            "modules": output["modules"],
            "workspace": output["workspace"],
            "tenant": output["tenant"],
            "manifest": output["manifest"],
            "release": output["release"],
            "validation": output["validation"]
        }


        output["report"] = self.report.generate(
            report_data
        )

        output["release_report"] = str(
            self.release_report.create(
                report_data
            )
        )


        self.state.set(
            "last_build",
            name
        )

        output["runtime"] = self.runtime.status()
        output["graph"] = self.graph.steps

        self.runtime.stop()

        return output
