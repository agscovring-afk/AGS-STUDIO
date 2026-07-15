"""
AGS-STUDIO Single Runtime Flow (v2 - Calibrated)
=================================================
المسار الموحد لتشغيل النظام.
معدّل ليتطابق مع أسماء الكلاسات والدوال الفعلية في المشروع.
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class RuntimeContext:
    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.results = {}
        self.start_time = time.time()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def elapsed(self):
        return time.time() - self.start_time

    def report(self):
        return {
            "timestamp": self.timestamp,
            "spec": self.spec,
            "stages": self.results,
            "elapsed_seconds": round(self.elapsed(), 2),
            "status": "success" if all(r.get("ok") for r in self.results.values() if r.get("ok") is not None) else "partial",
        }


def log_stage(name, ctx, ok, data=None):
    ctx.results[name] = {"ok": ok, "elapsed": round(ctx.elapsed(), 2), "data": data or {}}
    print(f"  {'OK' if ok else 'FAIL'}  {name:<25} ({ctx.elapsed():.2f}s)")


def stage_master(ctx):
    print("\n[1/8] Master Agent")
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from agents.master import MasterAgent
        agent = MasterAgent()
        result = agent.process_request(json.dumps(ctx.spec))
        log_stage("master_agent", ctx, True, {"status": "processed"})
        return True
    except Exception as e:
        log_stage("master_agent", ctx, False, {"error": str(e)})
        return False


def stage_planner(ctx):
    print("[2/8] Enterprise Planner")
    try:
        from enterprise_builder.planner.enterprise_planner import EnterprisePlanner
        p = EnterprisePlanner()
        result = p.analyze(json.dumps(ctx.spec))
        log_stage("planner", ctx, True, {"status": "analyzed"})
        return True
    except Exception as e:
        log_stage("planner", ctx, False, {"error": str(e)})
        return False


def stage_generator(ctx):
    print("[3/8] Generator")
    try:
        from enterprise_builder.generators.workspace_generator import WorkspaceGenerator
        g = WorkspaceGenerator()
        g.generate()
        log_stage("generator", ctx, True, {"status": "generated"})
        return True
    except Exception as e:
        log_stage("generator", ctx, False, {"error": str(e)})
        return False


def stage_executor(ctx):
    print("[4/8] Action Executor")
    try:
        from enterprise_builder.core.action_executor import EnterpriseActionExecutor
        e = EnterpriseActionExecutor()
        log_stage("executor", ctx, True, {"status": "ready"})
        return True
    except Exception as e:
        log_stage("executor", ctx, False, {"error": str(e)})
        return False


def stage_validator(ctx):
    print("[5/8] Validator")
    try:
        from enterprise_builder.core.enterprise_validator import EnterpriseValidator
        v = EnterpriseValidator()
        v.validate()
        log_stage("validator", ctx, True, {"status": "validated"})
        return True
    except Exception as e:
        log_stage("validator", ctx, False, {"error": str(e)})
        return False


def stage_healing(ctx):
    print("[6/8] Self-Healing")
    try:
        from enterprise_builder.healing.self_healing_engine import SelfHealingEngine
        h = SelfHealingEngine()
        log_stage("healing", ctx, True, {"status": "ready"})
        return True
    except Exception as e:
        log_stage("healing", ctx, False, {"error": str(e)})
        return False


def stage_production(ctx):
    print("[7/8] Production Guard")
    try:
        from enterprise_builder.core.production_guard import ProductionGuard
        g = ProductionGuard()
        g.check()
        log_stage("production_guard", ctx, True, {"status": "guarded"})
        return True
    except Exception as e:
        log_stage("production_guard", ctx, False, {"error": str(e)})
        return False


def stage_release(ctx):
    print("[8/8] Release Builder")
    try:
        from enterprise_builder.pipeline.release_builder import ReleaseBuilder
        r = ReleaseBuilder()
        r.build()
        log_stage("release", ctx, True, {"status": "released"})
        return True
    except Exception as e:
        log_stage("release", ctx, False, {"error": str(e)})
        return False


def run_flow(spec):
    print("=" * 60)
    print("AGS-STUDIO Runtime Flow v2")
    print("=" * 60)

    ctx = RuntimeContext(spec)
    stages = [stage_master, stage_planner, stage_generator, stage_executor,
              stage_validator, stage_healing, stage_production, stage_release]

    for s in stages:
        try:
            s(ctx)
        except Exception as e:
            print(f"  CRASH: {e}")

    print("\n" + "=" * 60)
    report = ctx.report()
    print(f"Status: {report['status']}  |  Time: {report['elapsed_seconds']}s")
    print("=" * 60)

    log_dir = Path(__file__).parent.parent.parent / "logs" / "runtime"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"flow_{ctx.timestamp}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Report: {log_file}")

    return report


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    args = ap.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        spec = json.load(f)

    report = run_flow(spec)
    sys.exit(0 if report["status"] == "success" else 1)


if __name__ == "__main__":
    main()
