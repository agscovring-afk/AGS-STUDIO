from app.repositories.financial_repository import FinancialRepository
from app.models.quotation import Quotation
from app.models.quotation_line import QuotationLine
from app.models.invoice import Invoice
from app.models.invoice_line import InvoiceLine
from app.models.payment import Payment
from datetime import datetime


class FinancialController:
    def __init__(self, repo: FinancialRepository):
        self.repo = repo

    def init_db(self):
        self.repo.create_tables()

    def generate_quotation_code(self, company_id: int) -> str:
        year = datetime.utcnow().year
        return self.repo.get_next_number(company_id, "DEV", year)

    def create_quotation(self, company_id: int, client_id: int, project_id: int = None, date: str = None, validity_date: str = None, lines: list = None) -> int:
        code = self.generate_quotation_code(company_id)
        q = Quotation(company_id=company_id, code=code, client_id=client_id, project_id=project_id, date=date or datetime.utcnow().isoformat(), validity_date=validity_date, status="draft")
        qid = self.repo.add_quotation(q)
        subtotal = 0.0
        if lines:
            for i, ln in enumerate(lines, start=1):
                total = ln['quantity'] * ln['unit_price']
                subtotal += total
                qline = QuotationLine(quotation_id=qid, line_no=i, item_type=ln.get('item_type','product'), item_id=ln.get('item_id'), description=ln.get('description',''), quantity=ln['quantity'], unit_price=ln['unit_price'], total=total)
                self.repo.add_quotation_line(qline)
        tax = 0.0
        total = subtotal + tax
        # Update totals by inserting an invoice record is out of scope here; we keep stored values minimal
        return qid

    def generate_invoice_code(self, company_id: int) -> str:
        year = datetime.utcnow().year
        return self.repo.get_next_number(company_id, "FAC", year)

    def create_invoice(self, company_id: int, client_id: int, project_id: int = None, date: str = None, due_date: str = None, lines: list = None) -> int:
        code = self.generate_invoice_code(company_id)
        inv = Invoice(company_id=company_id, code=code, client_id=client_id, project_id=project_id, date=date or datetime.utcnow().isoformat(), due_date=due_date, status="draft")
        iid = self.repo.add_invoice(inv)
        subtotal = 0.0
        if lines:
            for i, ln in enumerate(lines, start=1):
                total = ln['quantity'] * ln['unit_price']
                subtotal += total
                iline = InvoiceLine(invoice_id=iid, line_no=i, item_type=ln.get('item_type','product'), item_id=ln.get('item_id'), description=ln.get('description',''), quantity=ln['quantity'], unit_price=ln['unit_price'], total=total)
                self.repo.add_invoice_line(iline)
        tax = 0.0
        total = subtotal + tax
        return iid

    def record_payment(self, invoice_id: int, amount: float, date: str = None, method: str = "cash", reference: str = "") -> int:
        p = Payment(invoice_id=invoice_id, amount=amount, date=date or datetime.utcnow().isoformat(), method=method, reference=reference)
        return self.repo.add_payment(p)
