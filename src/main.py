from utils.env_detection import detect_virtual_environment
from utils.env_list_detection import detect_required_libraries_env, detect_installed_libraries

if __name__ == "__main__":
    dict_env = detect_virtual_environment()
    print("Detected environment:")
    for key, value in dict_env.items():
        print(f"{key}: {value}")

    required_libraries_env = detect_required_libraries_env()
    print("\nRequired libraries in env:")
    for package_name in required_libraries_env:
        print(f"- {package_name}")

    installed_libraries = detect_installed_libraries(dict_env["active_environment"])
    for package_name, package_version in installed_libraries.items():
        print(f"- {package_name}=={package_version}")

    required_librairies_with_version: dict[str, str] = {}
    for package_name in required_libraries_env:
        if package_name not in required_librairies_with_version and package_name in installed_libraries.keys():
            required_librairies_with_version[package_name] = installed_libraries[package_name]
    
    print("\nRequired libraries with version for requirements.txt:")
    for package_name, package_version in required_librairies_with_version.items():
        print(f"- {package_name}=={package_version}")
