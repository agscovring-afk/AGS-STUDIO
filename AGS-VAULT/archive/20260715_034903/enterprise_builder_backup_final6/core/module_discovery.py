from pathlib import Path


class ModuleDiscovery:

    def discover(self):

        modules = []

        path = Path("app/metadata/modules")

        if path.exists():

            for item in path.iterdir():

                if item.is_file():

                    modules.append(
                        item.stem
                    )

        return modules