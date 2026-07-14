from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Capability:
    """
    Represents a capability provided by an AGS-STUDIO component.
    """

    name: str

    category: str = ""

    description: str = ""

    provider: str = ""

    version: str = "1.0"

    enabled: bool = True

    discovered_at: datetime = field(
        default_factory=datetime.utcnow
    )

    requirements: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def add_requirement(
        self,
        requirement: str
    ) -> None:
        if requirement not in self.requirements:
            self.requirements.append(requirement)


@dataclass(slots=True)
class CapabilityRegistry:
    """
    Stores discovered capabilities.
    """

    capabilities: list[Capability] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def add(
        self,
        capability: Capability
    ) -> None:
        self.capabilities.append(capability)

    def count(self) -> int:
        return len(self.capabilities)

    def find(
        self,
        name: str
    ) -> Capability | None:
        for capability in self.capabilities:
            if capability.name == name:
                return capability

        return None
