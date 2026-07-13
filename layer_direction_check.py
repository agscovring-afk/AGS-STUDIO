from pathlib import Path

rules={
"models":["repositories","services","controllers","ui","ai"],
"repositories":["services","controllers","ui","ai"],
"services":["controllers","ui","ai"],
"controllers":["ui","ai"],
"ui":[],
"ai":[]
}

for layer,forbidden in rules.items():
    print("\n====",layer.upper(),"====")
    for f in Path("app/"+layer).rglob("*.py"):
        text=f.read_text(encoding="utf-8",errors="ignore")
        for target in forbidden:
            if f"app.{target}" in text:
                print(f"{f} -> imports {target}")
