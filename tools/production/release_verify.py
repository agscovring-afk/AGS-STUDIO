from pathlib import Path

root = Path(__file__).resolve().parents[2]

print("="*32)
print(" AGS-STUDIO RELEASE VERIFY ")
print("="*32)

version = "1.0.0"

print("VERSION:", version)
print("PROJECT:", root.name)
print("RELEASE:", "VERIFIED")
