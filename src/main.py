import os 
from pathlib import Path
from dotenv import load_dotenv

if __name__ == "__main__":
    env_path = Path(__file__).resolve().parents[1] / "infra" / "env"
    loaded = load_dotenv(dotenv_path=env_path)

    print(f"Hello {os.getenv('USER') }!")

    # Build a program that checks library versions installed in the venv.
    # Only retrieve versions for libraries listed in requirements.txt.
    # The program must display versions of libraries installed in the venv.
    # The program must display versions of libraries listed in requirements.txt.
    # Apply the same logic based on detected virtual environment: venv or conda.