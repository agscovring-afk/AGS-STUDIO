from datetime import datetime


class EnterpriseManifest:

    def generate(self, name):

        return {
            "enterprise": name,
            "created": datetime.now().isoformat(),
            "version": "1.0"
        }
