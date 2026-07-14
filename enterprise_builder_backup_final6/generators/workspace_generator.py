from pathlib import Path


class WorkspaceGenerator:

    def generate(self):

        folders = [
            "enterprise_output/workspace",
            "enterprise_output/modules",
            "enterprise_output/reports",
            "enterprise_output/releases"
        ]

        for folder in folders:

            Path(folder).mkdir(
                parents=True,
                exist_ok=True
            )

        return {
            "workspace": "created"
        }