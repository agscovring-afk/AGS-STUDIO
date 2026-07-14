
import importlib

class Router:

    @classmethod
    def load_registry(cls):
        pass

    @classmethod
    def load(cls,route,parent):

        modules={
        "dashboard":"dashboard_page",
        "companies":"companies_page",
        "users":"users_page",
        "projects":"projects_page",
        "inventory":"inventory_page",
        "finance":"finance_page",
        "reports":"reports_page",
        "ai_builder":"ai_builder_page",
        "autonomous":"autonomous_page"
        }

        if route not in modules:
            return None

        m=importlib.import_module(
            "app.ui.pages."+modules[route]
        )

        for obj in m.__dict__.values():
            if isinstance(obj,type) and obj.__module__==m.__name__:
                return obj(parent)

        return None
