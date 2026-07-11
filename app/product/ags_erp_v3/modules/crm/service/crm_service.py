class CRMModule:

    name = "CRM"

    def __init__(self):
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def list_customers(self):
        return self.customers
