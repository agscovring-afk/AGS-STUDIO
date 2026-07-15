class PageGenerator:


    def generate(self, entity):

        name = entity.name.capitalize()


        return {
            "page": f"{name}Page",
            "route": f"/{entity.name}",
            "title": name
        }
