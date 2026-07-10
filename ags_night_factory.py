from pathlib import Path
import json
import time
from datetime import datetime


BASE = Path("night_build")


tasks = [

    {
        "name": "architecture",
        "output": "architecture/tender_architecture.json",
        "data": {
            "module": "Tender Management",
            "layers": [
                "AI Layer",
                "Business Layer",
                "Database Layer",
                "API Layer",
                "UI Layer"
            ]
        }
    },

    {
        "name": "database",
        "output": "database/tender_schema.json",
        "data": {
            "tables": [
                "tenders",
                "clients",
                "documents",
                "boq_items",
                "suppliers",
                "supplier_quotes",
                "evaluations",
                "contracts"
            ]
        }
    },

    {
        "name": "agents",
        "output": "agents/tender_agents.json",
        "data": {
            "agents": [
                "Tender Analyzer Agent",
                "Document Reader Agent",
                "BOQ Extractor Agent",
                "Pricing Agent",
                "Risk Agent",
                "Report Agent"
            ]
        }
    },

    {
        "name": "backend",
        "output": "backend/backend_plan.json",
        "data": {
            "modules": [
                "Tender Service",
                "Document Service",
                "BOQ Service",
                "Evaluation Service"
            ]
        }
    },

    {
        "name": "ui",
        "output": "ui/ui_plan.json",
        "data": {
            "screens": [
                "Tender Dashboard",
                "Tender Details",
                "BOQ Viewer",
                "AI Analysis"
            ]
        }
    },

    {
        "name": "testing",
        "output": "tests/test_plan.json",
        "data": {
            "tests": [
                "Tender CRUD",
                "Document Upload",
                "BOQ Processing",
                "AI Analysis"
            ]
        }
    },

]


def write_task(task):

    path = BASE / task["output"]

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(
            task["data"],
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


report = {
    "project": "AGS Tender Management",
    "started": str(datetime.now()),
    "tasks": []
}


print("""
================================
 AGS NIGHT AUTONOMOUS FACTORY
================================
""")


for task in tasks:

    print(
        "Running:",
        task["name"]
    )

    time.sleep(2)

    write_task(task)

    report["tasks"].append(
        {
            "task": task["name"],
            "status": "completed"
        }
    )

    print(
        task["name"],
        "DONE"
    )


(BASE / "report").mkdir(
    exist_ok=True
)


(BASE / "report/night_report.json").write_text(
    json.dumps(
        report,
        indent=4,
        ensure_ascii=False
    ),
    encoding="utf-8"
)


print("""
================================
 NIGHT BUILD COMPLETED
 Report:
 night_build/report/night_report.json
================================
""")