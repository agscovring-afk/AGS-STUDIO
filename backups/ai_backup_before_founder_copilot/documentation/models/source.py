from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class SourceFile:
    """
    Represents a discovered source file in the project.
    """

    path: Path
    relative_path: str

    name: str
    extension: str

    size: int = 0

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    modified_at: datetime = field(
        default_factory=datetime.utcnow
    )

    checksum: str = ""

    analyzed: bool = False

    is_python: bool = False

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def mark_analyzed(self) -> None:
        self.analyzed = True

    def set_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        return self.metadata.get(key, default)


@dataclass(slots=True)
class FileCollection:
    """
    Collection container used by scanners.
    """

    files: list[SourceFile] = field(
        default_factory=list
    )

    def add(self, source_file: SourceFile) -> None:
        self.files.append(source_file)

    def count(self) -> int:
        return len(self.files)

    def python_files(self) -> list[SourceFile]:
        return [
            file
            for file in self.files
            if file.is_python
        ]
