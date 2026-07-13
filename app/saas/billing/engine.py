class BillingEngine:

    def generate_invoice(self,tenant_id):

        return {
            "tenant_id":tenant_id,
            "status":"generated"
        }
