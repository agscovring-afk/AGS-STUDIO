
import json,os


class ERPFactoryV1:

    def execute(self,request):

        blueprint={
            'engine':'AGS ERP FACTORY ENGINE V1',
            'status':'COMPLETED',
            'erp_modules':[
                'projects',
                'finance',
                'inventory',
                'hr',
                'crm'
            ]
        }

        json.dump(
            blueprint,
            open('data/erp_blueprint.json','w'),
            indent=4
        )

        return blueprint


bridge=ERPFactoryV1()
