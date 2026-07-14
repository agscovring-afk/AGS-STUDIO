class PermissionEngine:

    def __init__(self):
        self.permissions = {}

    def grant(self, role, permission):
        self.permissions.setdefault(role, []).append(permission)

    def check(self, role, permission):
        return permission in self.permissions.get(role, [])
