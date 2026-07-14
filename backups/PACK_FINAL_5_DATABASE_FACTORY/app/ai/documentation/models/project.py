from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class DocumentationConfiguration:
    project_root: Path
    docs_root: Path
    output_database: Path

    include_patterns: tuple[str, ...] = ("*.py",)

    exclude_directories: tuple[str, ...] = (
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "build",
        "dist",
    )

    follow_symlinks: bool = False
    recursive: bool = True

    generate_markdown: bool = True
    generate_html: bool = True
    generate_database: bool = True


@dataclass(slots=True)
class ProjectStatistics:
    scanned_files: int = 0
    scanned_directories: int = 0

    python_files: int = 0

    classes: int = 0
    functions: int = 0

    imports: int = 0
    dependencies: int = 0

    services: int = 0
    modules: int = 0

    agents: int = 0
    providers: int = 0
    plugins: int = 0

    pages: int = 0
    commands: int = 0

    warnings: int = 0
    errors: int = 0


@dataclass(slots=True)
class ProjectMetadata:
    name: str
    version: str = "2.0"

    author: str = ""
    description: str = ""

    python_version: str = ""
    platform: str = ""

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class ProjectInfo:
    metadata: ProjectMetadata
    configuration: DocumentationConfiguration

    statistics: ProjectStatistics = field(
        default_factory=ProjectStatistics
    )

    session_id: str = ""
    build_id: str = ""

    attributes: dict[str, Any] = field(
        default_factory=dict
    )

    def touch(self) -> None:
        self.metadata.updated_at = datetime.utcnow()

    def set(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.attributes.get(key, default)
