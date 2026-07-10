from .team import team
from .task_share import task_pool, SharedTask
from .report import report


class CollaborationManager:

    def register_agent(self, name, role):
        agent = team.add_agent(
            name,
            role
        )

        report.add(
            f"Agent registered: {name}"
        )

        return agent


    def create_task(self, name, description, priority=1):

        task = SharedTask(
            name,
            description,
            priority
        )

        task_pool.add(task)

        report.add(
            f"Task created: {name}"
        )

        return task


    def assign_task(self, task_name, agent_name):

        agent = team.get_agent(agent_name)

        for task in task_pool.tasks:

            if task.name == task_name:

                task.assign(agent_name)

                if agent:
                    agent.assign_task(task_name)

                report.add(
                    f"{task_name} assigned to {agent_name}"
                )

                return True

        return False


    def status(self):

        return {
            "team": team.list_agents(),

            "tasks": [
                {
                    "name": task.name,
                    "status": task.status,
                    "agent": task.assigned_to
                }
                for task in task_pool.tasks
            ],

            "report": report.generate()
        }


manager = CollaborationManager()