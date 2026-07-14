from pathlib import Path


class SecurityConfig:

    BASE_DIR = Path(__file__).parent

    SECURITY_ENABLED = True
    AUDIT_ENABLED = True
    POLICY_ENGINE_ENABLED = True
