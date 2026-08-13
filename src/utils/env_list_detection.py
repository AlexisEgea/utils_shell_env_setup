from importlib.metadata import distributions
import json
import os
import shutil
import subprocess

def detect_required_libraries_env() -> list[str]:
    """Read required package names from infra/requirements.txt."""
    installed_libraries = []
    path_env = os.path.join(os.getcwd(), "infra", "requirements.txt")
    with open(path_env, "r") as file:
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

def detect_installed_libraries_conda() -> dict[str, str]:
    """List installed packages from the active Conda environment."""
    installed = {}

    conda_cmd = os.getenv("CONDA_EXE") or shutil.which("conda")
    if conda_cmd:
        try:
            result = subprocess.run(
                [conda_cmd, "list", "--json"],
                capture_output=True,
                text=True,
                check=True,
            )
            packages = json.loads(result.stdout)
            for package in packages:
                package_name = package.get("name")
                package_version = package.get("version")
                if package_name:
                    installed[package_name] = package_version or "unknown-version"
            return installed
        except (subprocess.SubprocessError, json.JSONDecodeError):
            pass

    return installed

def detect_installed_libraries(activ_env: str) -> dict[str, str]:
    """Detect installed libraries from the active environment."""
    installed_libraries: dict[str, str] = dict[str, str]()
    if activ_env == "venv":
        print("\nInstalled libraries in venv:")
        installed_libraries = detect_installed_libraries_venv()
        
    elif activ_env == "conda":
        print("\nInstalled libraries in conda:")
        installed_libraries = detect_installed_libraries_conda()

    return installed_libraries