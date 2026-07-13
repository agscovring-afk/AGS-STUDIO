class OrganizationService:

    def create(self, tenant_id, name):

        return {
            "tenant_id": tenant_id,
            "name": name
        }
