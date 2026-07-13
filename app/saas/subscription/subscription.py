class Subscription:

    def __init__(self, tenant_id, plan):
        self.tenant_id = tenant_id
        self.plan = plan
        self.status = "active"
