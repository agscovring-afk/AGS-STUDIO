from pathlib import Path
import re

roots=["models","repositories","services","controllers","ui","ai"]

for root in roots:
    print(f"\n===== {root.upper()} IMPORT CHECK =====")
    for f in Path("app/"+root).rglob("*.py"):
        text=f.read_text(encoding="utf-8",errors="ignore")
        imports=re.findall(r"(?:from|import)\s+(app\.[\w\.]+)",text)
        if imports:
            print(f"\n{f}")
            for i in sorted(set(imports)):
                print(" ->",i)
