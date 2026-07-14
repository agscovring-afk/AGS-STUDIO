class IdentityContext:

    def __init__(self):
        self.user = None
        self.roles = []

    def authenticate(self, user):
        self.user = user
        return True
