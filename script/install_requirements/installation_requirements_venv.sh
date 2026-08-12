#!/bin/bash

project_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo project_directory: $project_directory
echo script_directory: $script_directory

# Function to display a success message
print_success() {
  # Print a standardized success line for detected tools.
  echo "✔ $1 is installed: $2"
}

# Function to display an error message with download link and pause
exit_error() {
  # Exit after showing a generic prerequisite error message.
  echo "Script stopped. Please install the missing prerequisite and rerun the script."
  read -p ""
  exit 1
}

echo "-----------------------------------------------------------------------------"
echo "|                          Installation Requirements                        |"
echo "| Author : Alexis EGEA                                                      |"
echo "-----------------------------------------------------------------------------"

# Detecting the OS and determining the appropriate Python command
echo "OS detected: $OSTYPE"
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    PYTHON_CMD=python3
elif [[ "$OSTYPE" == "cygwin"* || "$OSTYPE" == "msys"* ]]; then
    PYTHON_CMD=python
else
    echo "Unsupported OS '$OSTYPE'"
    exit 1
fi
echo

echo "_____________________________________________________________________________"
# Checking Python version with the required version from utils/required_tools_versions.sh file
echo "Checking Python..."
python_version="3.11"
if command -v $PYTHON_CMD &>/dev/null; then
  PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
  # if result == required version 
  # (meaning the detected version is greater than or equal to the required version), 
  if [[ "$(printf '%s\n%s\n' "$python_version" "$PYTHON_VERSION" | sort -V | awk 'NR==1')" == "$python_version" ]]; then
    echo "✅ Python is installed: $PYTHON_VERSION (required: >= $python_version)"
  else
    echo "❌ Python version is too old: $PYTHON_VERSION (required: >= $python_version)"
    echo "Download Python here: https://www.python.org/downloads"
    echo "Important: Check the box to 'Add Python version to PATH' during installation to make the new version accessible via the python command."
    exit_error
  fi
else
  echo "❌ Python (version >= $python_version required) is not installed."
  echo "Download it here: https://www.python.org/downloads"
  echo "Important: Check the box to 'Add Python version to PATH' during installation to make the new version accessible via the python command."
  exit_error
fi

echo "_____________________________________________________________________________"
echo "Creating virtual environment..."
if [[ -d "$project_directory/venv" ]]; then
  echo "ℹ️ Virtual environment 'venv' is already created."
else
  $PYTHON_CMD -m venv "$project_directory/venv" && echo "✅ Virtual environment created." || { read -p "❌ Failed to create virtual environment."; exit 1; }
fi

echo "_____________________________________________________________________________"
echo "Activating virtual environment..."

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    source "$project_directory/venv/bin/activate"
elif [[ "$OSTYPE" == "cygwin"* || "$OSTYPE" == "msys"* ]]; then
    source "$project_directory/venv/Scripts/activate"
else
    read -p "❌ Cannot activate virtual environment for OS: $OSTYPE"
    exit 1
fi
echo "✅ Virtual environment activated."

echo "_____________________________________________________________________________"
echo "Installing requirements from requirements.txt..."
pip install -r "$project_directory/infra/requirements.txt" || { read -p "❌ Failed to install dependencies"; exit 1; }
echo "✅ Requirements installed."
echo

echo "_____________________________________________________________________________"
echo "Making launcher scripts executable..."
cd "$project_directory/script/launch_program"
for script in *.sh; do
  chmod +x "$script"
  echo "$script"
done
echo "✅ Scripts executable"

echo
echo "🎉 Done! Project is ready to be executed."
read -p "Press any key to close the terminal window..."