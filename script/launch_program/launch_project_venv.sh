#!/bin/bash

project_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
venv_directory="$project_directory/venv"

echo "-----------------------------------------------------------------------------"
echo "|                        Launch Project with venv                           |"
echo "| Author : Alexis EGEA                                                      |"
echo "-----------------------------------------------------------------------------"
echo

echo "Project directory: $project_directory"
echo

if [ ! -d "$venv_directory" ]; then
  echo "Virtual environment not found: $venv_directory"
  echo "Please run script/installation_requirement.sh first."
  read -p "Press any key to close the terminal window..."
  exit 1
fi

echo "_____________________________________________________________________________"
echo "Activating virtual environment..."
echo "OS detected: $OSTYPE"

if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
  activate_script="$venv_directory/bin/activate"
elif [[ "$OSTYPE" == "cygwin"* || "$OSTYPE" == "msys"* ]]; then
  activate_script="$venv_directory/Scripts/activate"
else
  echo "Unsupported OS '$OSTYPE'"
  read -p "Press any key to close the terminal window..."
  exit 1
fi

if [ ! -f "$activate_script" ]; then
  echo "Activation script not found: $activate_script"
  read -p "Press any key to close the terminal window..."
  exit 1
fi

source "$activate_script"
echo "Virtual environment activated."
echo

echo "_____________________________________________________________________________"
echo "Launching project..."
echo
python "$project_directory/src/main.py"

