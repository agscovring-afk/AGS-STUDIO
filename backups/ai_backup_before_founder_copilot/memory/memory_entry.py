from datetime import datetime
from typing import Any, Dict, Optional

from app.ai.memory.memory_types import MemoryType


class MemoryEntry:
    """
    Standard memory object.
    """

    def __init__(
        self,
        content: Any,
        memory_type: MemoryType,
        module: Optional[str] = None,
        agent: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):

        self.id = datetime.now().timestamp()

        self.created_at = str(
            datetime.now()
        )

        self.type = memory_type.value

        self.module = module

        self.agent = agent

        self.content = content

        self.metadata = metadata or {}


    def to_dict(self):

        return {
            "id": self.id,
            "created_at": self.created_at,
            "type": self.type,
            "module": self.module,
            "agent": self.agent,
            "content": self.content,
            "metadata": self.metadata
        }