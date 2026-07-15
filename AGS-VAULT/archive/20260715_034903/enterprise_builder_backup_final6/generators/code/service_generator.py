class ServiceGenerator:


    def generate(self, entity):

        name = entity.name.capitalize()


        return f'''
class {name}Service:


    def create(self, data):

        return data


    def list(self):

        return []
'''
