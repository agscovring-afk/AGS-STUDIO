from .crm.crm_module import CRMModule
from .projects.projects_module import ProjectsModule
from .suppliers.suppliers_module import SuppliersModule
from .inventory.inventory_module import InventoryModule
from .purchasing.purchasing_module import PurchasingModule
from .quotations.quotations_module import QuotationsModule
from .invoices.invoices_module import InvoicesModule
from .accounting.accounting_module import AccountingModule
from .hr.hr_module import HRModule
from .reports.reports_module import ReportsModule


ERP_MODULES = [
    CRMModule,
    ProjectsModule,
    SuppliersModule,
    InventoryModule,
    PurchasingModule,
    QuotationsModule,
    InvoicesModule,
    AccountingModule,
    HRModule,
    ReportsModule,
]
