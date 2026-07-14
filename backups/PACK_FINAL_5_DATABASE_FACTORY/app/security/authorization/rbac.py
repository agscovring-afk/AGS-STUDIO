class RBACManager:

    def __init__(self):
        self.roles={}

    def add_role(self, name, permissions):
        self.roles[name]=permissions
