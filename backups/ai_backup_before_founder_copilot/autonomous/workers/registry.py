from .erp_builder_worker import ERPBuilderWorker
from .module_builder_worker import ModuleBuilderWorker
from .file_creator_worker import FileCreatorWorker
from .architect_worker import ArchitectWorker
from .database_worker import DatabaseWorker
from .backend_worker import BackendWorker
from .ui_worker import UIWorker
from .scanner_worker import ScannerWorker
from .validator_worker import ValidatorWorker
from .fixer_worker import FixerWorker


class WorkerRegistry:


    def __init__(self):

        self.workers = {

            "architect":
            ArchitectWorker(),

            "database":
            DatabaseWorker(),

            "backend":
            BackendWorker(),

            "ui":
            UIWorker(),

            "file_creator":
            FileCreatorWorker(),

            "module_builder":
            ModuleBuilderWorker(),

            "erp_builder":
            ERPBuilderWorker(),

            "scanner":
            ScannerWorker(),

            "validator":
            ValidatorWorker(),

            "fixer":
            FixerWorker()

        }


    def get(self,name):

        return self.workers.get(name)



registry = WorkerRegistry()
