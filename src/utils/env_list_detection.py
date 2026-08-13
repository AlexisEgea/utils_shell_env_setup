from importlib.metadata import distributions
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

def detect_required_libraries_env() -> list[str]:
    """Read required package names from infra/requirements.txt."""
    installed_libraries = []
    # Build path from this file location to avoid cwd-dependent errors.
    path_env = Path(__file__).resolve().parents[2] / "infra" / "requirements.txt"
    with open(path_env, "r", encoding="utf-8") as file:
        for line in file:
            package_name = line.strip()
            installed_libraries.append(package_name)
    return installed_libraries
    

def detect_installed_libraries_venv() -> dict[str, str]:
    """List installed packages from the current Python environment (venv case)."""
    installed = {}
    for dist in distributions():
        name = dist.metadata.get("Name") or dist.metadata.get("Summary") or "unknown-package"
        version = dist.version or "unknown-version"
        installed[name] = version

    return installed

def get_conda_env_prefix() -> Path | None:
    """Resolve the Conda env prefix from activation vars or the running interpreter."""
    conda_prefix = os.getenv("CONDA_PREFIX")
    if conda_prefix:
        return Path(conda_prefix)

    prefix = Path(sys.prefix).resolve()
    if (prefix / "conda-meta").is_dir():
        return prefix
    return None


def get_conda_env_name(prefix: Path | None) -> str:
    """Resolve the Conda env name from activation vars or the prefix path."""
    conda_default_env = os.getenv("CONDA_DEFAULT_ENV")
    if conda_default_env:
        return conda_default_env
    if prefix is None:
        return "unknown"
    if prefix.parent.name == "envs":
        return prefix.name
    return "base"


def find_conda_executable(prefix: Path | None) -> str | None:
    """Locate conda even when the shell was not activated."""
    conda_cmd = os.getenv("CONDA_EXE") or shutil.which("conda")
    if conda_cmd:
        return conda_cmd
    if prefix is None:
        return None

    # Named env: <root>/envs/<name> -> conda lives in <root>, not in the env.
    roots = [prefix]
    if prefix.parent.name == "envs":
        roots.append(prefix.parent.parent)

    relative_candidates = (
        ("Scripts", "conda.exe"),
        ("condabin", "conda.exe"),
        ("condabin", "conda.bat"),
        ("bin", "conda"),
    )
    for root in roots:
        for parts in relative_candidates:
            candidate = root.joinpath(*parts)
            if candidate.is_file():
                return str(candidate)
    return None


def get_installed_from_conda_meta(prefix: Path) -> dict[str, str]:
    """Read package names/versions from conda-meta when the conda CLI is unavailable."""
    installed: dict[str, str] = {}
    meta_dir = prefix / "conda-meta"
    if not meta_dir.is_dir():
        return installed

    for meta_file in meta_dir.glob("*.json"):
        try:
            with open(meta_file, encoding="utf-8") as file:
                package = json.load(file)
        except (OSError, json.JSONDecodeError):
            continue
        package_name = package.get("name")
        if package_name:
            installed[package_name] = package.get("version") or "unknown-version"
    return installed


def detect_installed_libraries_conda() -> dict[str, str]:
    """List installed packages from the active Conda environment."""
    prefix = get_conda_env_prefix()
    conda_cmd = find_conda_executable(prefix)

    if conda_cmd:
        command = [conda_cmd, "list", "--json"]
        if prefix is not None:
            command.extend(["--prefix", str(prefix)])
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )
            packages = json.loads(result.stdout)
            installed = {}
            for package in packages:
                package_name = package.get("name")
                package_version = package.get("version")
                if package_name:
                    installed[package_name] = package_version or "unknown-version"
            return installed
        except (subprocess.SubprocessError, json.JSONDecodeError, OSError):
            pass

    if prefix is not None:
        return get_installed_from_conda_meta(prefix)
    return {}

def detect_installed_libraries(activ_env: str) -> dict[str, str]:
    """Detect installed libraries from the active environment."""
    installed_libraries: dict[str, str] = dict[str, str]()
    if activ_env == "venv":
        print("\nInstalled libraries in venv:")
        installed_libraries = detect_installed_libraries_venv()
        
    elif activ_env == "conda":
        conda_env_name = get_conda_env_name(get_conda_env_prefix())
        print(f"\nInstalled libraries in conda ({conda_env_name}):")
        installed_libraries = detect_installed_libraries_conda()

    return installed_libraries