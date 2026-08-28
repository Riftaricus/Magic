import subprocess
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent
VENV_DIR = BASE_DIR / "venv"
VENV_PYTHON_WINDOWS = VENV_DIR / "Scripts" / "python.exe"
VENV_PYTHON_LINUX = VENV_DIR / "bin" / "python"

def install(run: bool):
    print("Attempting to update git repository")
    try:
        subprocess.run(["git", "pull"])
    except Exception:
        print("Failed to update git repository, skipping step")

    print("Attempting to create venv folder")
    try:
        subprocess.run(["py", "-m", "venv", "venv"])
    except FileNotFoundError:
        print("Py has not been found, trying python3")
        subprocess.run(["python3", "-m", "venv", "venv"])
    print("Succesfully created .venv")
    used_python = ""
    if VENV_DIR.exists():
        try:
            print("Trying windows install of requirements")
            subprocess.run([VENV_PYTHON_WINDOWS, "-m", "pip", "install", "-r", "requirements.txt"])
            used_python = VENV_PYTHON_WINDOWS
        except FileNotFoundError:
            print("Failed windows install of requirements")
            print("Trying linux install of requirements")
            subprocess.run([VENV_PYTHON_LINUX, "-m", "pip", "install", "-r", "requirements.txt"])
            used_python = VENV_PYTHON_LINUX
    if run:
        print("Attempting to run code")
        subprocess.run([used_python, "main.py"])
if len(sys.argv) > 1:
    install(True if sys.argv[1] == "run" else False)
else:
    install(False)