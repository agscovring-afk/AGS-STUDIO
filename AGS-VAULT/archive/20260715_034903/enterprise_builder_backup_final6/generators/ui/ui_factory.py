from .page_generator import PageGenerator
from .form_generator import FormGenerator
from .dashboard_generator import DashboardGenerator
from .menu_generator import MenuGenerator


class UIFactory:


    def __init__(self):

        self.pages = PageGenerator()
        self.forms = FormGenerator()
        self.dashboards = DashboardGenerator()
        self.menus = MenuGenerator()


    def generate(self, metadata):

        result = {}

        for entity in metadata["entities"]:

            result[entity.name] = {
                "page": self.pages.generate(entity),
                "form": self.forms.generate(entity),
                "dashboard": self.dashboards.generate(entity),
                "menu": self.menus.generate(entity)
            }

        return result
