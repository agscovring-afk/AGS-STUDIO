class RepositoryGenerator:


    def generate(self, entity):

        name = entity.name.capitalize()


        return f'''
class {name}Repository:


    def create(self, data):

        return data


    def get_all(self):

        return []
'''
