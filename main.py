"""Project entry point."""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"


def _relaunch_with_venv_if_needed() -> None:
    """Use the project virtual environment when system Python is active."""
    if not VENV_PYTHON.exists():
        return

    if Path(sys.executable).resolve() == VENV_PYTHON.resolve():
        return

    command = [str(VENV_PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]]
    raise SystemExit(subprocess.call(command))


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    _relaunch_with_venv_if_needed()

    try:
        from src.main import main
    except ModuleNotFoundError as error:
        print("Nedostaju Python paketi za ovaj projekt.")
        print(f"Greška: {error}")
        if VENV_PYTHON.exists():
            print(f"Koristi projektni environment: {VENV_PYTHON} main.py")
        else:
            print("Prvo kreiraj environment: python -m venv .venv")
            print("Zatim instaliraj pakete: .venv\\Scripts\\pip install -r requirements.txt")
        raise SystemExit(1) from error

    main()
