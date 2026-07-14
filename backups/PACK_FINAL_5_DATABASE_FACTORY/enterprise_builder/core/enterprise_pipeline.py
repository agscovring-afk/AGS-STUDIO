from enterprise_builder.core.enterprise_generator import EnterpriseGenerator
from enterprise_builder.core.enterprise_manifest import EnterpriseManifest
from enterprise_builder.core.enterprise_registry import EnterpriseRegistry
from enterprise_builder.core.enterprise_config import EnterpriseConfig
from enterprise_builder.core.module_discovery import ModuleDiscovery
from enterprise_builder.core.tenant_foundation import TenantFoundation
from enterprise_builder.generators.workspace_generator import WorkspaceGenerator
from enterprise_builder.pipeline.release_builder import ReleaseBuilder

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
        ):
            self.graph.add(step)

        output = {}

        output["generator"] = self.generator.create()
        output["config"] = self.config.load()
        output["modules"] = self.discovery.discover()
        output["workspace"] = self.workspace.generate()
        output["tenant"] = self.tenant.create()
        output["manifest"] = self.manifest.generate(name)

        self.registry.register(name, output["manifest"])

        output["release"] = self.release.build()

        self.state.set("last_build", name)

        output["runtime"] = self.runtime.status()
        output["graph"] = self.graph.steps

        self.runtime.stop()

        return output
