from ags.pipeline.build_context import BuildContext


class Pipeline:


    def __init__(self, agent_manager):

        self.agent_manager = agent_manager



    def run(self, module):

        context = BuildContext(module)


        print()
        print("=" * 45)
        print("      AGS AI BUILD PIPELINE V2")
        print("=" * 45)
        print()


        agents = [

            "architect",
            "backend",
            "database",
            "ui",
            "testing",
            "documentation"

        ]


        for index, agent in enumerate(agents, 1):

            try:

                print(
                    f"[{index}/6] {agent}"
                )


                result = self.agent_manager.run(
                    agent,
                    module
                )


                context.add_result(
                    agent,
                    result
                )


                context.log(
                    f"{agent} completed"
                )


                print(
                    f"{agent} OK"
                )


            except Exception as error:

                context.error(
                    f"{agent}: {error}"
                )

                print(
                    f"{agent} FAILED"
                )


        print()

        print("PIPELINE FINISHED")


        return context
