class ModelGenerator:


    def generate(self, entity):

        class_name = entity.name.capitalize()


        fields = "\n".join(
            [
                f"    {field}: str"
                for field in entity.fields
            ]
        )


        return f'''
class {class_name}Model:


    def __init__(self):

{fields}
'''
