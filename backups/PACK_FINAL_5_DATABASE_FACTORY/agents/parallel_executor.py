from concurrent.futures import ThreadPoolExecutor, as_completed


class ParallelExecutor:


    def __init__(self, manager):

        self.manager = manager



    def run(self, agents, request):

        results = {}


        with ThreadPoolExecutor(
            max_workers=len(agents)
        ) as executor:


            tasks = {}

            for agent in agents:

                tasks[
                    executor.submit(
                        self.manager.run,
                        agent,
                        request
                    )
                ] = agent



            for future in as_completed(tasks):

                agent = tasks[future]

                try:
                    results[agent] = future.result()

                except Exception as e:

                    results[agent] = {
                        "error": str(e)
                    }


        return results
