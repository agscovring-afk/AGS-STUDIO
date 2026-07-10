"""
app/ai/autonomous/knowledge.py
"""

from __future__ import annotations


class AutonomousKnowledge:

    def __init__(self):
        self.knowledge = {}

    def add(self, key, value):

        self.knowledge[key] = value

        return True

    def get(self, key, default=None):

        return self.knowledge.get(
            key,
            default
        )

    def search(self, keyword):

        results = {}

        for key, value in self.knowledge.items():

            if keyword.lower() in key.lower():

                results[key] = value

        return results

    def all(self):

        return self.knowledge