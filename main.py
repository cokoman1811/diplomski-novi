"""Project entry point."""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
REQUIREMENTS = PROJECT_ROOT / "requirements.txt"


def _venv_python() -> Path:
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def _run(command: list[str]) -> None:
    subprocess.check_call(command, cwd=PROJECT_ROOT)


def _install_requirements(python: Path) -> None:
    if not REQUIREMENTS.exists():
        return

    print("Instaliram pakete iz requirements.txt...")
    _run([str(python), "-m", "pip", "install", "-q", "--upgrade", "pip"])
    _run([str(python), "-m", "pip", "install", "-q", "-r", str(REQUIREMENTS)])


def _ensure_venv() -> Path:
    """Create .venv on first run."""
    python = _venv_python()

    if not python.exists():
        print("Kreiram virtualno okruženje (.venv)...")
        _run([sys.executable, "-m", "venv", str(VENV_DIR)])
        _install_requirements(python)

    return python


def _relaunch_with_venv_if_needed(python: Path) -> None:
    """Use the project virtual environment when system Python is active."""
    if Path(sys.executable).resolve() == python.resolve():
        return

    command = [str(python), str(Path(__file__).resolve()), *sys.argv[1:]]
    raise SystemExit(subprocess.call(command))


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    venv_python = _ensure_venv()
    _relaunch_with_venv_if_needed(venv_python)

    try:
        from src.main import main
    except ModuleNotFoundError:
        _install_requirements(venv_python)
        from src.main import main

    main()
