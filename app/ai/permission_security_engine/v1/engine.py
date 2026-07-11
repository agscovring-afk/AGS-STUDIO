from .permission_manager import PermissionManager
from .role_engine import RoleEngine
from .security_validator import SecurityValidator


class PermissionSecurityEngine:

    def __init__(self):
        self.name = "PERMISSION_SECURITY_ENGINE_V1"
        self.permissions = PermissionManager()
        self.roles = RoleEngine()
        self.validator = SecurityValidator()

    def execute(self, data):

        role = self.roles.resolve(
            data.get("role", "admin")
        )

        permission = self.permissions.check(
            data.get("user", "system"),
            data.get("permission", "all")
        )

        security = self.validator.validate(data)

        return {
            "engine": self.name,
            "role": role,
            "permission": permission,
            "security": security,
            "status": "COMPLETED"
        }

    def status(self):
        return {
            "engine": self.name,
            "status": "READY"
        }
