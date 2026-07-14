"""
app/ai/autonomous/project_analyzer.py
"""

from __future__ import annotations

from collections import Counter

from .context import AutonomousContext


class ProjectAnalyzer:

    def __init__(self, context: AutonomousContext):
        self.context = context

    def analyze(self):

        files = self.context.snapshot.files

        extensions = Counter()

        total_size = 0

        for file in files:
            extensions[file.extension] += 1
            total_size += file.size

        report = {
            "total_files": len(files),
            "total_size": total_size,
            "extensions": dict(extensions),
        }

        self.context.snapshot.statistics.update(report)

        return report

    def python_files(self):

        return [
            f
            for f in self.context.snapshot.files
            if f.extension == ".py"
        ]

    def count_python_files(self):

        return len(self.python_files())