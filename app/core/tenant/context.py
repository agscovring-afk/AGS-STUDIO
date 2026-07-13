class TenantContext:

    _tenant_id = None

    @classmethod
    def set(cls, tenant_id):
        cls._tenant_id = tenant_id

    @classmethod
    def get(cls):
        return cls._tenant_id

    @classmethod
    def clear(cls):
        cls._tenant_id = None
