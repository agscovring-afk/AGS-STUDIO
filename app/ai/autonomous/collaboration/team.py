from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgentMember:

    name: str
    role: str
    status: str = "IDLE"
    current_task: str = None
    joined_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


    def assign_task(self, task):

        self.current_task = task
        self.status = "WORKING"


    def complete_task(self):

        self.status = "COMPLETED"



class AgentTeam:


    def __init__(self, name="AGS AUTONOMOUS TEAM"):

        self.name = name
        self.members = []


    def add_agent(self, name, role):

        agent = AgentMember(
            name=name,
            role=role
        )

        self.members.append(agent)

        return agent



    def get_agent(self, name):

        for agent in self.members:

            if agent.name == name:
                return agent

        return None



    def list_agents(self):

        return [

            {
                "name": agent.name,
                "role": agent.role,
                "status": agent.status,
                "task": agent.current_task
            }

            for agent in self.members

        ]



team = AgentTeam()