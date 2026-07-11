
import json


class ConstructionPackV1:

    def execute(self,request):

        template={
            'engine':'AGS CONSTRUCTION INDUSTRY PACK V1',
            'status':'COMPLETED',
            'domain':'Construction ERP',
            'specialization':[
                'Contracting',
                'Facade',
                'Aluminium',
                'Curtain Wall'
            ]
        }

        json.dump(
            template,
            open('data/construction_erp_template.json','w'),
            indent=4
        )

        return template


bridge=ConstructionPackV1()
