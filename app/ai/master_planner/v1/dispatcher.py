from .runner import run_production

class BuildDispatcher:

    def dispatch(self, target):

        if target in (
            "production",
            "full-production",
            "all",
        ):
            return run_production()

        return None
