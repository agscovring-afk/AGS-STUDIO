from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AgentMessage:
    sender: str
    receiver: str
    action: str
    payload: Any = None
    priority: int = 1
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "action": self.action,
            "payload": self.payload,
            "priority": self.priority,
            "created_at": self.created_at,
        }