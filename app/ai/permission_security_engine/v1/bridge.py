from .engine import PermissionSecurityEngine


class PermissionSecurityBridge:

    def __init__(self):
        self.engine = PermissionSecurityEngine()

    def execute(self, data):
        return self.engine.execute(data)

    def status(self):
        return self.engine.status()


permission_security_engine = PermissionSecurityBridge()
