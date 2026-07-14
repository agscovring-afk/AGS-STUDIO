class ProjectScanner:

    def scan(self, project):

        return {
            "project": project,
            "status": "scanned",
            "files": [],
            "modules": []
        }
