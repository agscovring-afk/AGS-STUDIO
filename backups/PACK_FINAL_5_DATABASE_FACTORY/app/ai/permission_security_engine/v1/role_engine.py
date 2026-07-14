class RoleEngine:

    def __init__(self):
        self.name = "ROLE_ENGINE_V1"

    def resolve(self, role):
        return {
            "role": role,
            "permissions": [
                "create",
                "read",
                "update",
                "delete"
            ]
        }
