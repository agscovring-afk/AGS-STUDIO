class ControllerGenerator:


    def generate(self, entity):

        name = entity.name.capitalize()


        return f'''
class {name}Controller:


    def index(self):

        return []
'''
