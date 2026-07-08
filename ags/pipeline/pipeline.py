from ags.pipeline.build_context import BuildContext
from ags.ai.session.manager import AISessionManager
from ags.generator.ai_code_generator import AICodeGenerator


class Pipeline:


    def __init__(self, agent_manager):

        self.agent_manager = agent_manager
        self.session_manager = AISessionManager()
        self.generator = AICodeGenerator()


    def run(self, module):

        print("""
=============================================
      AGS AI BUILD PIPELINE V5
=============================================
""")


        context = BuildContext(module)

        session = self.session_manager.create(
            module
        )


        agents = [

            "architect",
            "backend",
            "database",
            "ui",
            "testing",
            "documentation"

        ]


        for index, agent in enumerate(agents, 1):

            print(
                f"[{index}/6] {agent}"
            )


            try:

                result = self.agent_manager.run(
                    agent,
                    module,
                    session
                )


                context.add_result(
                    agent,
                    result
                )


                print(
                    agent,
                    "OK"
                )


            except Exception as e:

                context.add_error(
                    str(e)
                )

                print(
                    agent,
                    "FAILED"
                )


        context.metadata["ai_session"] = session.to_dict()


        print()
        print(
            "Generating AI Output..."
        )


        output = self.generator.generate(
            module,
            context
        )


        context.metadata["generated"] = output


        print()
        print(
            "PIPELINE V5 FINISHED"
        )


        return context
