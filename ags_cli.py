#!/usr/bin/env python3
"""AGS-STUDIO CLI v2.1 - Unified with Workflow Generator"""
import sys, os, json, argparse, subprocess
from pathlib import Path
from datetime import datetime


class C:
    R = "\033[91m"; G = "\033[92m"; Y = "\033[93m"
    C = "\033[96m"; X = "\033[0m"; BOLD = "\033[1m"


def banner():
    print(f"\n{C.C}{C.BOLD}========================================{C.X}")
    print(f"{C.C}{C.BOLD}    AGS-STUDIO v2.1 - Unified CLI{C.X}")
    print(f"{C.C}{C.BOLD}========================================{C.X}\n")


def cmd_run(args):
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"{C.R}Spec not found:{C.X} {spec_path}")
        return 1
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    print(f"{C.C}Running Runtime Flow for:{C.X} {spec_path.name}\n")
    sys.path.insert(0, str(Path(__file__).parent))
    from ags.runtime import flow
    report = flow.run_flow(spec)
    return 0 if report["status"] == "success" else 1


def cmd_status(args):
    root = Path.cwd()
    print(f"{C.C}Project Status{C.X}\n" + "=" * 40)
    print(f"  Root:         {root}")
    print(f"  Date:         {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    py = [f for f in root.rglob("*.py") if ".venv" not in str(f) and "__pycache__" not in str(f)]
    print(f"  Python files: {len(py)}")
    log_dir = root / "logs" / "runtime"
    if log_dir.exists():
        logs = list(log_dir.glob("*.json"))
        print(f"  Runtime logs: {len(logs)}")
    vault = root / "AGS-VAULT"
    if vault.exists():
        vf = [f for f in vault.rglob("*") if f.is_file()]
        print(f"  Vault items:  {len(vf)} files")
    return 0


def cmd_doctor(args):
    root = Path.cwd()
    print(f"{C.C}Project Health Check{C.X}\n" + "=" * 40)
    checks = [
        ((root / "agents" / "master.py").exists(), "Master Agent"),
        ((root / "enterprise_builder").exists(), "Enterprise Builder"),
        ((root / "AGS-VAULT").exists(), "AGS-VAULT"),
        ((root / "ags" / "runtime" / "flow.py").exists(), "Runtime Flow"),
        ((root / "ags" / "runtime" / "workflow_gen.py").exists(), "Workflow Generator"),
        ((root / "gap_analysis.py").exists(), "Gap Analysis"),
        ((root / "cleanup_ags_studio.py").exists(), "Cleanup Script"),
    ]
    for ok, name in checks:
        print(f"  [{C.G}OK{C.X}]   {name}" if ok else f"  [{C.R}NO{C.X}]   {name}")
    p = sum(1 for ok, _ in checks if ok)
    print(f"\nResult: {p}/{len(checks)} passed")
    return 0 if p == len(checks) else 1


def cmd_gap(args):
    print(f"{C.C}Running Gap Analysis...{C.X}\n")
    r = subprocess.run([sys.executable, "gap_analysis.py", str(Path.cwd())], capture_output=True, text=True)
    print(r.stdout)
    return r.returncode


def cmd_workflow(args):
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"{C.R}Spec not found:{C.X} {spec_path}")
        return 1
    print(f"{C.C}Generating workflows for:{C.X} {spec_path.name}\n")
    wg = Path(__file__).parent / "ags" / "runtime" / "workflow_gen.py"
    r = subprocess.run([sys.executable, str(wg), "--spec", str(spec_path)], capture_output=True, text=True)
    print(r.stdout)
    if r.stderr:
        print(f"{C.Y}{r.stderr}{C.X}")
    return r.returncode


def cmd_help(args):
    banner()
    print(f"{C.BOLD}Commands:{C.X}")
    print(f"  {C.G}run{C.X} --spec <file>       تشغيل Runtime Flow")
    print(f"  {C.G}workflow{C.X} --spec <file>  توليد Workflows تلقائية")
    print(f"  {C.G}status{C.X}                 حالة المشروع")
    print(f"  {C.G}doctor{C.X}                 فحص صحة المشروع")
    print(f"  {C.G}gap{C.X}                    تحليل الفجوات")
    print(f"  {C.G}help{C.X}                   عرض المساعدة")
    return 0


def main():
    p = argparse.ArgumentParser(prog="ags", add_help=False)
    s = p.add_subparsers(dest="cmd")
    s.add_parser("help")
    s.add_parser("status")
    s.add_parser("doctor")
    s.add_parser("gap")
    for n in ["run", "flow"]:
        sp = s.add_parser(n)
        sp.add_argument("--spec", required=True)
    sp_wf = s.add_parser("workflow")
    sp_wf.add_argument("--spec", required=True)
    args = p.parse_args()
    if not args.cmd:
        return cmd_help(args)
    cmds = {
        "run": cmd_run, "flow": cmd_run, "status": cmd_status,
        "doctor": cmd_doctor, "gap": cmd_gap, "workflow": cmd_workflow,
        "help": cmd_help,
    }
    return cmds.get(args.cmd, cmd_help)(args)


if __name__ == "__main__":
    sys.exit(main())