from .message import AgentMessage


class AgentBus:
    """
    Central communication bus between autonomous agents
    """

    def __init__(self):
        self.messages = []
        self.history = []

    def send(self, message: AgentMessage):
        self.messages.append(message)

        self.history.append({
            "type": "SEND",
            "message": message.to_dict()
        })

        return {
            "status": "DELIVERED",
            "from": message.sender,
            "to": message.receiver,
            "action": message.action
        }

    def receive(self, agent_name: str):
        received = [
            msg for msg in self.messages
            if msg.receiver == agent_name
        ]

        self.messages = [
            msg for msg in self.messages
            if msg.receiver != agent_name
        ]

        return received

    def broadcast(self, sender: str, action: str, payload=None):
        message = AgentMessage(
            sender=sender,
            receiver="ALL",
            action=action,
            payload=payload
        )

        return self.send(message)

    def stats(self):
        return {
            "queued_messages": len(self.messages),
            "history_count": len(self.history)
        }


bus = AgentBus()