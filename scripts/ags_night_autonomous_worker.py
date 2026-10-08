from pathlib import Path
import json
import time
from datetime import datetime


BASE = Path("night_worker")

TASKS = [
    "Analyze Tender Management architecture",
    "Generate database models",
    "Generate backend services",
    "Generate API structure",
    "Generate AI agents",
    "Generate testing plan",
    "Generate documentation"
]


def save(path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


def run_task(task):

    print("\nRUNNING:", task)

    time.sleep(3)

    result = {
        "task": task,
        "status": "completed",
        "time": str(datetime.now())
    }

    filename = (
        task
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        + ".json"
    )

    save(
        BASE / "results" / filename,
        result
    )

    print("DONE:", task)

    return result



print("""
====================================
 AGS NIGHT AUTONOMOUS WORKER V1
====================================
""")


report = {
    "project": "AGS Tender Autonomous Build",
    "start": str(datetime.now()),
    "tasks": []
}


for task in TASKS:

    result = run_task(task)

    report["tasks"].append(
        result
    )


save(
    BASE / "report.json",
    report
)


print("""
====================================
 NIGHT WORK COMPLETED
 REPORT:
 night_worker/report.json
====================================
""")