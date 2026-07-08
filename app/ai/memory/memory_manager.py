import json
import os

from typing import List

from app.ai.memory.memory_entry import MemoryEntry
from app.ai.memory.memory_types import MemoryType


MEMORY_FILE = "app/ai/memory/project_memory.json"


class MemoryManager:
    """
    AGS Memory Engine Core.
    """

    def __init__(self):

        folder = os.path.dirname(
            MEMORY_FILE
        )

        os.makedirs(
            folder,
            exist_ok=True
        )

        if not os.path.exists(
            MEMORY_FILE
        ):
            self.save([])


    # ==========================
    # Storage
    # ==========================

    def load(self):

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    def save(self, data):

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )


    # ==========================
    # Remember
    # ==========================

    def remember(
        self,
        content,
        memory_type=MemoryType.PROJECT,
        module=None,
        agent=None,
        metadata=None
    ):

        memory = self.load()

        entry = MemoryEntry(
            content=content,
            memory_type=memory_type,
            module=module,
            agent=agent,
            metadata=metadata
        )


        memory.append(
            entry.to_dict()
        )


        self.save(
            memory
        )

        return entry.to_dict()


    # ==========================
    # Search
    # ==========================

    def search(
        self,
        keyword
    ):

        memory = self.load()

        result = []

        for item in memory:

            text = str(
                item.get(
                    "content",
                    ""
                )
            )

            if keyword.lower() in text.lower():

                result.append(
                    item
                )

        return result


    # ==========================
    # By Type
    # ==========================

    def get_by_type(
        self,
        memory_type
    ):

        memory = self.load()

        return [

            item for item in memory

            if item.get("type")
            ==
            memory_type.value

        ]


    # ==========================
    # Module Memory
    # ==========================

    def get_module_memory(
        self,
        module
    ):

        memory = self.load()

        return [

            item for item in memory

            if item.get("module")
            ==
            module

        ]


    # ==========================
    # Agent Memory
    # ==========================

    def get_agent_memory(
        self,
        agent
    ):

        memory = self.load()

        return [

            item for item in memory

            if item.get("agent")
            ==
            agent

        ]


    # ==========================
    # Conversation Memory
    # ==========================

    def get_conversation_memory(
        self
    ):

        return self.get_by_type(
            MemoryType.CONVERSATION
        )


memory_manager = MemoryManager()