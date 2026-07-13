from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ImportInfo:
    """
    Represents an import statement discovered in a Python file.
    """

    module: str

    name: str = ""

    alias: str = ""

    import_type: str = "import"

    line_number: int = 0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class Dependency:
    """
    Represents a dependency relationship between project components.
    """

    source: str

    target: str

    dependency_type: str = "import"

    strength: float = 1.0

    description: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def set_metadata(
        self,
        key: str,
        value: Any
    ) -> None:
        self.metadata[key] = value


@dataclass(slots=True)
class DependencyGraphNode:
    """
    Node representation used by dependency graph builders.
    """

    identifier: str

    node_type: str

    name: str = ""

    path: str = ""

    dependencies: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def add_dependency(
        self,
        target: str
    ) -> None:
        if target not in self.dependencies:
            self.dependencies.append(target)


@dataclass(slots=True)
class DependencyGraph:
    """
    In-memory dependency graph model.
    """

    nodes: dict[str, DependencyGraphNode] = field(
        default_factory=dict
    )

    relations: list[Dependency] = field(
        default_factory=list
    )

    def add_node(
        self,
        node: DependencyGraphNode
    ) -> None:
        self.nodes[node.identifier] = node

    def add_relation(
        self,
        dependency: Dependency
    ) -> None:
        self.relations.append(dependency)

    def node_count(self) -> int:
        return len(self.nodes)

    def relation_count(self) -> int:
        return len(self.relations)
