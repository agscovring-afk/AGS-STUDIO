class DomainAnalyzer:

    def analyze(self, request: str):

        text = request.lower()

        profile = "general"

        if any(
            x in text
            for x in [
                "facade",
                "construction",
                "aluminium",
                "curtain wall",
                "glass",
                "building"
            ]
        ):
            profile = "construction_facade"

        elif any(
            x in text
            for x in [
                "erp",
                "enterprise",
                "business"
            ]
        ):
            profile = "enterprise"

        return {
            "profile": profile,
            "request": request
        }
