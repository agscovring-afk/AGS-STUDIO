class UsageMeter:

    def record(self,tenant_id,event):

        return {
            "tenant_id":tenant_id,
            "event":event
        }
