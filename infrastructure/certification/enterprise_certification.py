from tests.enterprise.enterprise_validation import *

class EnterpriseCertification:

    def run(self):

        tests = [
            EnterpriseArchitectureValidator(),
            CloudLayerValidator(),
            APILayerValidator(),
            MultiTenantValidator(),
            AutonomousValidator(),
            MarketplaceValidator(),
            GlobalReleaseValidator()
        ]

        results = {}

        for test in tests:
            results.update(test.validate())

        results["certification"] = "ENTERPRISE CERTIFIED"

        return results


if __name__ == "__main__":
    print(EnterpriseCertification().run())
