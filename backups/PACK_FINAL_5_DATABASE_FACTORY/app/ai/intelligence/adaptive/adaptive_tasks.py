"""
AGS Adaptive Task Intelligence
"""

from datetime import datetime


class AdaptiveTaskIntelligence:


    def adapt(self, request, decision, lesson):

        tasks_profile = "standard"


        text = request.lower()


        if "construction" in text or "facade" in text or "erp" in text:
            tasks_profile = "enterprise_construction"


        if decision.get(
            "recommended_action"
        ) == "reuse_previous_knowledge":

            mode="optimized"

        else:
            mode="discovery"


        return {

            "profile":
            tasks_profile,


            "mode":
            mode,


            "strategy":

            [
                "reuse_architecture"
                if mode=="optimized"
                else
                "analyze_domain",

                "generate_metadata",

                "create_modules",

                "run_validation"
            ],


            "created":
            str(datetime.now())
        }



adaptive_intelligence = AdaptiveTaskIntelligence()
