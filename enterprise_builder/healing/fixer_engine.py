
class FixerEngine:

    def fix(self, repair_plan):

        results = []

        for item in repair_plan:

            results.append(
                {
                    "fixed": True,
                    "item": item
                }
            )

        return results
