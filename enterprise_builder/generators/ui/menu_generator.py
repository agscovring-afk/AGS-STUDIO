class MenuGenerator:


    def generate(self, entity):

        return {
            "menu": entity.name,
            "icon": "default",
            "visible": True
        }
