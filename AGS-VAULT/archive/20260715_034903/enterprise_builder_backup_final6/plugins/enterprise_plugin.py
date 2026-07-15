
from enterprise_builder.core.enterprise_pipeline import EnterprisePipeline
from enterprise_builder.plugins.enterprise_doctor import EnterpriseDoctor
from enterprise_builder.pipeline.release_builder import ReleaseBuilder


class EnterprisePlugin:


    def __init__(self):

        self.pipeline = EnterprisePipeline()

        self.doctor = EnterpriseDoctor()

        self.release = ReleaseBuilder()



    def build(self, *args):

        name = (
            args[0]
            if args
            else "AGS_ENTERPRISE"
        )

        result = self.pipeline.execute(name)

        print("ENTERPRISE BUILD COMPLETED")

        print(result)

        return result



    def run_doctor(self, *args):

        result = self.doctor.run()

        print("ENTERPRISE DOCTOR COMPLETED")

        print(result)

        return result



    def run_release(self, *args):

        result = self.release.build()

        print("ENTERPRISE RELEASE COMPLETED")

        print(result)

        return result



def register(command_manager):

    plugin = EnterprisePlugin()


    command_manager.register(
        "enterprise",
        lambda *args: dispatch(
            plugin,
            *args
        )
    )



def dispatch(plugin, *args):

    if not args:

        return plugin.build()


    command = args[0]

    params = args[1:]


    if command == "build":

        return plugin.build(
            *params
        )


    if command == "doctor":

        return plugin.run_doctor(
            *params
        )


    if command == "release":

        return plugin.run_release(
            *params
        )


    print(
        "Unknown enterprise command:",
        command
    )
