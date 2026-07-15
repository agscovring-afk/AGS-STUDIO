import json
from pathlib import Path


class TenantFoundation:

    def create(self):

        data = {
            "tenant_mode": True,
            "tenants": []
        }

        Path(
            "enterprise_output/tenants.json"
        ).write_text(
            json.dumps(data, indent=4)
        )

        return data