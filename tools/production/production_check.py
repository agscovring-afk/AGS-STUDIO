from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]

def check(path, name):
    status = "OK" if path.exists() else "MISSING"
    return f"{name}: {status}"

print("="*32)
print(" AGS-STUDIO PRODUCTION CHECK ")
print("="*32)

checks = [
    (BASE / "ags.yaml", "CONFIG"),
    (BASE / "ags.py", "CORE"),
    (BASE / "ags_studio.db", "DATABASE"),
    (BASE / "app/ai", "AI ENGINE"),
    (BASE / "app/registry", "REGISTRY"),
    (BASE / "app/metadata", "METADATA"),
    (BASE / "app/security", "SECURITY"),
    (BASE / "app/ai/autonomous", "AUTONOMOUS")
]

for p,n in checks:
    print(check(p,n))

print()
print("STATUS: PRODUCTION VALIDATION COMPLETE")

