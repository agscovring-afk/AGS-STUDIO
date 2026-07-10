from pathlib import Path

p = Path("ags/plugins/ask.py")

s = p.read_text(encoding="utf-8")

old = '''    print()

    print("MASTER COMPLETED")'''

new = '''    print()

    print(result)

    print()

    print("MASTER COMPLETED")'''

if old in s:
    s = s.replace(old, new)

p.write_text(s, encoding="utf-8")

print("ask fixed")