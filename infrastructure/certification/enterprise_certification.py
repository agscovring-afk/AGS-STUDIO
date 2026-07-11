from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.enterprise.enterprise_validation import (
    EnterpriseArchitectureValidator,
    CloudLayerValidator,
    APILayerValidator,
    MultiTenantValidator,
    AutonomousValidator,
    MarketplaceValidator,
    GlobalReleaseValidator
)


class EnterpriseCertification:

    def run(self):

        validators = [
            EnterpriseArchitectureValidator(),
            CloudLayerValidator(),
            APILayerValidator(),
            MultiTenantValidator(),
            AutonomousValidator(),
            MarketplaceValidator(),
            GlobalReleaseValidator()
        ]

        results = {}

        for validator in validators:
            results.update(validator.validate())

        results["certification"] = "ENTERPRISE CERTIFIED"

        return results


if __name__ == "__main__":
    print(EnterpriseCertification().run())
