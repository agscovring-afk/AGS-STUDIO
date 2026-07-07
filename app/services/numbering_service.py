"""
AGS ERP V2
Numbering Service
"""

from datetime import datetime


class NumberingService:

    def __init__(self):
        self.counters = {}

    def generate(
        self,
        document_type,
        prefix,
        padding=5,
        yearly=False
    ):
        year = datetime.now().year

        key = document_type

        if yearly:
            key = f"{document_type}_{year}"

        current = self.counters.get(key, 0) + 1

        self.counters[key] = current

        number = str(current).zfill(padding)

        if yearly:
            return f"{prefix}-{year}-{number}"

        return f"{prefix}-{number}"

    def reset(self, document_type):
        if document_type in self.counters:
            del self.counters[document_type]