from app.ai.memory.project_memory import memory as project_memory
from app.ai.memory.decision_memory import memory as decision_memory
from app.ai.memory.agent_memory import memory as agent_memory
from app.ai.memory.knowledge_store import store


class MemoryEngine:


    def status(self):

        return {
            "system":
            "AGS MEMORY ENGINE",

            "modules":[
                "PROJECT_MEMORY",
                "DECISION_MEMORY",
                "AGENT_MEMORY",
                "KNOWLEDGE_STORE"
            ],

            "status":
            "ACTIVE"
        }


engine = MemoryEngine()
