from .crud.engine import CRUDController
from .database.engine import ProductionDatabase
from .modules.business_modules import *


class AGSERPV3ProductionRuntime:


    def boot(self):

        db = ProductionDatabase()

        return {
            "database": db.connect(),
            "migration": db.migrate(),
            "crud": CRUDController().create(
                {"module":"ERP V3"}
            ),
            "modules":[
                CRMModule().start(),
                ProjectsModule().start(),
                InventoryModule().start(),
                InvoiceModule().start(),
                ReportsModule().start()
            ]
        }
