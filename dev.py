import sys
import subprocess

def run(cmd):
    print(">>>", " ".join(cmd))
    subprocess.run(cmd)

def doctor():
    run(["python", "ags.py", "doctor"])

def build(module):
    run(["python", "ags.py", "ai", "build", module])

def create(module):
    run(["python", "ags.py", "ai", "create", module])

def repair():
    run(["python", "ags.py", "doctor"])

def test():
    run(["python", "-m", "pytest"])

def release():
    run(["git", "add", "."])
    run(["git", "commit", "-m", "Automatic Release"])

def help_menu():
    print("""
AGS-STUDIO Developer CLI

Commands:
python dev.py doctor
python dev.py build <module>
python dev.py create <module>
python dev.py repair
python dev.py test
python dev.py release
""")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        help_menu()
        sys.exit()

    cmd = sys.argv[1]

    if cmd == "doctor":
        doctor()

    elif cmd == "build":
        build(sys.argv[2])

    elif cmd == "create":
        create(sys.argv[2])

    elif cmd == "repair":
        repair()

    elif cmd == "test":
        test()

    elif cmd == "release":
        release()

    else:
        help_menu()
