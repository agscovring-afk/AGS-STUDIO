class LicenseEngine:

    def validate(self,subscription):

        return subscription.status=="active"
