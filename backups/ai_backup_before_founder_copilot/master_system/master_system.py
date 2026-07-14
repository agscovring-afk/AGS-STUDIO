from app.ai.master_system.autonomous_core import core
from app.ai.master_system.multi_agents import agents
from app.ai.master_system.erp_generator import generator


class MasterSystem:


    def status(self):

        return {

            "system":
            "AGS AUTONOMOUS MASTER SYSTEM",

            "core":
            core.status(),

            "agents":
            agents.status(),

            "factory":
            "CONNECTED",

            "erp_generator":
            generator.generate(
                "CONSTRUCTION ERP"
            ),

            "status":
            "ONLINE"
        }


master = MasterSystem()
