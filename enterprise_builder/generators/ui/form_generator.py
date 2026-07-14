class FormGenerator:


    def generate(self, entity):

        return {
            "form": f"{entity.name}_form",
            "fields": entity.fields
        }
