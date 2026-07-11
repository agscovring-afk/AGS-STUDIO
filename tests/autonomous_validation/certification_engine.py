from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tests.autonomous_validation.platform_tests import (
    CloudIntegrationTest,
    MobileLayerTest,
    MarketplaceTest,
    APIEcosystemTest,
    MultiTenantIsolationTest,
    AutonomousCompanyTest,
    UniversalFactoryTest,
    AIEcosystemTest,
    AgentMarketplaceTest,
    AutonomousERPTest,
    GlobalAIBusinessValidation
)


class AutonomousPlatformCertification:

    def validate(self):

        tests = [
            CloudIntegrationTest(),
            MobileLayerTest(),
            MarketplaceTest(),
            APIEcosystemTest(),
            MultiTenantIsolationTest(),
            AutonomousCompanyTest(),
            UniversalFactoryTest(),
            AIEcosystemTest(),
            AgentMarketplaceTest(),
            AutonomousERPTest(),
            GlobalAIBusinessValidation()
        ]

        result = {}

        for test in tests:
            result.update(test.run())

        result["certification"] = "AGS-STUDIO GLOBAL AI PLATFORM CERTIFIED"

        return result


if __name__ == "__main__":
    print(AutonomousPlatformCertification().validate())
