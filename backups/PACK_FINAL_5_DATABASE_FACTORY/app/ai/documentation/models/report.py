from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class ReportItem:
    """
    Represents a single report message.
    """

    level: str

    message: str

    source: str = ""

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class DocumentationReport:
    """
    Complete documentation execution report.
    """

    title: str

    status: str = "PENDING"

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    finished_at: datetime | None = None

    files_generated: list[str] = field(
        default_factory=list
    )

    items: list[ReportItem] = field(
        default_factory=list
    )

    statistics: dict[str, Any] = field(
        default_factory=dict
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def add_item(
        self,
        item: ReportItem
    ) -> None:
        self.items.append(item)

    def add_file(
        self,
        file_path: str
    ) -> None:
        self.files_generated.append(file_path)

    def complete(
        self
    ) -> None:
        self.status = "COMPLETED"
        self.finished_at = datetime.utcnow()
