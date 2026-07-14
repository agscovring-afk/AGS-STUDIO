class PriorityEngine:


    def calculate(self, tasks):

        result = []

        priority = 10

        for task in tasks:

            result.append({
                "task": task,
                "priority": priority
            })

            priority -= 1


        return result


engine = PriorityEngine()
