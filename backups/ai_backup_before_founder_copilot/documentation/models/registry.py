from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class RegistryEntry:
    """
    Represents a registered AGS-STUDIO component.
    """

    name: str

    component_type: str

    module_path: str = ""

    version: str = "1.0"

    description: str = ""

    enabled: bool = True

    discovered_at: datetime = field(
        default_factory=datetime.utcnow
    )

    capabilities: list[str] = field(
        default_factory=list
    )

    dependencies: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def add_capability(
        self,
        capability: str
    ) -> None:
        if capability not in self.capabilities:
            self.capabilities.append(capability)

    def add_dependency(
        self,
        dependency: str
    ) -> None:
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)


@dataclass(slots=True)
class RegistrySnapshot:
    """
    Snapshot of the complete AI Registry state.
    """

    entries: list[RegistryEntry] = field(
        default_factory=list
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def add(
        self,
        entry: RegistryEntry
    ) -> None:
        self.entries.append(entry)

    def count(self) -> int:
        return len(self.entries)

    def find(
        self,
        name: str
    ) -> RegistryEntry | None:
        for entry in self.entries:
            if entry.name == name:
                return entry

        return None
