from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .project import ProjectInfo
from .source import FileCollection
from .dependency import DependencyGraph
from .registry import RegistrySnapshot
from .capability import CapabilityRegistry
from .report import DocumentationReport


@dataclass(slots=True)
class DocumentationSnapshot:
    """
    Complete runtime snapshot of Documentation Engine state.
    """

    project: ProjectInfo

    sources: FileCollection = field(
        default_factory=FileCollection
    )

    dependencies: DependencyGraph = field(
        default_factory=DependencyGraph
    )

    registry: RegistrySnapshot = field(
        default_factory=RegistrySnapshot
    )

    capabilities: CapabilityRegistry = field(
        default_factory=CapabilityRegistry
    )

    reports: list[DocumentationReport] = field(
        default_factory=list
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def add_report(
        self,
        report: DocumentationReport
    ) -> None:
        self.reports.append(report)

    def set_metadata(
        self,
        key: str,
        value: Any
    ) -> None:
        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        return self.metadata.get(key, default)
