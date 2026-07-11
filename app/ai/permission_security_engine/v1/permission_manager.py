class PermissionManager:

    def __init__(self):
        self.name = "PERMISSION_MANAGER_V1"

    def check(self, user, permission):
        return {
            "user": user,
            "permission": permission,
            "allowed": True
        }
