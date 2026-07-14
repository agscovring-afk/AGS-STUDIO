from .bus import bus
from .message import AgentMessage


class AgentChannel:
    """
    Communication channel wrapper for agents
    """

    def __init__(self, agent_name):
        self.agent_name = agent_name

    def send_to(self, receiver, action, payload=None, priority=1):
        message = AgentMessage(
            sender=self.agent_name,
            receiver=receiver,
            action=action,
            payload=payload,
            priority=priority
        )

        return bus.send(message)

    def listen(self):
        messages = bus.receive(self.agent_name)

        return [
            msg.to_dict()
            for msg in messages
        ]

    def broadcast(self, action, payload=None):
        return bus.broadcast(
            self.agent_name,
            action,
            payload
        )