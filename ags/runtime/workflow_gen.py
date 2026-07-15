"""AGS-STUDIO Workflow Generator v1"""
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


WORKFLOW_TEMPLATES = {
    "invoice_payment": {
        "trigger": "invoice.status == 'paid'",
        "actions": [
            "update client.balance -= invoice.amount",
            "create accounting_entry (debit: cash, credit: revenue)",
            "notify project_manager via email",
        ],
    },
    "project_completion": {
        "trigger": "project.status == 'completed'",
        "actions": [
            "archive all project_invoices",
            "calculate final_costs = sum(invoices) + sum(expenses)",
            "close related purchase_orders",
            "generate completion_report.pdf",
        ],
    },
    "stock_below_threshold": {
        "trigger": "stock.quantity < stock.threshold",
        "actions": [
            "create purchase_request (quantity = threshold * 2)",
            "notify procurement_team",
            "block orders requiring this stock",
        ],
    },
    "client_overdue": {
        "trigger": "invoice.due_date < today AND invoice.status == 'pending'",
        "actions": [
            "send reminder_email to client",
            "create follow_up_task for sales_team",
            "calculate late_fee (5pct per week)",
        ],
    },
    "employee_onboarding": {
        "trigger": "employee.status == 'new'",
        "actions": [
            "create user_account",
            "assign default_role = 'employee'",
            "send welcome_email with credentials",
            "schedule orientation_meeting",
        ],
    },
}


def generate_workflow(modules):
    workflows = []
    names = [m.get("name", "").lower() for m in (modules if isinstance(modules, list) else [modules])]
    if "invoice" in names and "client" in names:
        workflows.append({"name": "invoice_payment", **WORKFLOW_TEMPLATES["invoice_payment"]})
    if "project" in names:
        workflows.append({"name": "project_completion", **WORKFLOW_TEMPLATES["project_completion"]})
    if "stock" in names or "inventory" in names:
        workflows.append({"name": "stock_below_threshold", **WORKFLOW_TEMPLATES["stock_below_threshold"]})
    if "invoice" in names and "client" in names:
        workflows.append({"name": "client_overdue", **WORKFLOW_TEMPLATES["client_overdue"]})
    if "employee" in names or "hr" in names:
        workflows.append({"name": "employee_onboarding", **WORKFLOW_TEMPLATES["employee_onboarding"]})
    return {
        "generated_at": datetime.now().isoformat(),
        "modules_count": len(names),
        "workflows_count": len(workflows),
        "workflows": workflows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    args = ap.parse_args()
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Spec not found: {spec_path}")
        return 1
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    modules = spec.get("modules", [spec])
    result = generate_workflow(modules)
    print("")
    print("=== Workflow Generator ===")
    print(f"Modules: {result['modules_count']}")
    print(f"Generated: {result['workflows_count']} workflows")
    print("")
    for w in result["workflows"]:
        print(f"[WF] {w['name']}")
        print(f"     Trigger: {w['trigger']}")
        for a in w["actions"]:
            print(f"     -> {a}")
        print("")
    out_dir = Path("generated/workflows")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"workflows_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())