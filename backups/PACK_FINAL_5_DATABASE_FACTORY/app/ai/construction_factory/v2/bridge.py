
class ConstructionERPFactoryV2:

    def execute(self,request):

        return {
            "engine":"AGS CONSTRUCTION ERP FACTORY V2",
            "modules":[
                "Projects",
                "Contracts",
                "BOQ",
                "Estimation",
                "Cost Control",
                "Procurement",
                "Facade",
                "Aluminium"
            ],
            "status":"COMPLETED"
        }


bridge=ConstructionERPFactoryV2()
