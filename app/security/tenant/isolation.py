class TenantIsolationEngine:

    def validate(self, record_tenant_id, current_tenant_id):

        if record_tenant_id != current_tenant_id:
            raise PermissionError(
                'Tenant isolation violation'
            )

        return True
