import os
from pathlib import Path
import sys

def detect_virtual_environment_venv(prefix_path: Path, base_prefix_path: Path) -> dict:
    """Detect whether a venv-style environment is active and return its markers."""
    virtual_env = os.getenv("VIRTUAL_ENV")
    has_pyvenv_cfg = (prefix_path / "pyvenv.cfg").is_file()
    isolated_prefix = str(prefix_path) != str(base_prefix_path)

    is_active = bool(virtual_env) or has_pyvenv_cfg or isolated_prefix
    detected_path = virtual_env or (str(prefix_path) if has_pyvenv_cfg or isolated_prefix else None)

    return {
        "is_active": is_active,
        "path": detected_path,
        "has_pyvenv_cfg": has_pyvenv_cfg,
        "is_isolated_prefix": isolated_prefix,
    }

def detect_virtual_environment_conda(prefix_path: Path) -> dict:
    """Detect whether a Conda environment is active and return its markers."""
    conda_default_env = os.getenv("CONDA_DEFAULT_ENV")
    conda_prefix = os.getenv("CONDA_PREFIX")
    has_conda_meta = (prefix_path / "conda-meta").is_dir()

    is_active = bool(conda_default_env or conda_prefix or has_conda_meta)

    return {
        "is_active": is_active,
        "default_env": conda_default_env,
        "prefix": conda_prefix,
        "has_conda_meta": has_conda_meta,
    }

def detect_virtual_environment() -> dict:
    """Combine venv and Conda signals and return a normalized environment report."""
    info = {}

    prefix_path = Path(sys.prefix).resolve()
    base_prefix_path = Path(getattr(sys, "base_prefix", sys.prefix)).resolve()

    venv_info = detect_virtual_environment_venv(prefix_path, base_prefix_path)
    conda_info = detect_virtual_environment_conda(prefix_path)

    # In mixed cases (e.g. conda base + active venv), prioritize active venv.
    if venv_info["is_active"]:
        active_environment = "venv"
    elif conda_info["is_active"]:
        active_environment = "conda"
    else:
        active_environment = "none"

    info["active_environment"] = active_environment
    info["venv_active"] = venv_info["is_active"]
    info["venv"] = venv_info["path"]
    info["has_pyvenv_cfg"] = venv_info["has_pyvenv_cfg"]
    info["is_isolated_prefix"] = venv_info["is_isolated_prefix"]
    info["conda_active"] = conda_info["is_active"]
    info["conda_default_env"] = conda_info["default_env"]
    info["conda_prefix"] = conda_info["prefix"]
    info["has_conda_meta"] = conda_info["has_conda_meta"]
    info["python_executable"] = str(Path(sys.executable).resolve())
    info["python_prefix"] = str(prefix_path)
    info["python_base_prefix"] = str(base_prefix_path)

    return info