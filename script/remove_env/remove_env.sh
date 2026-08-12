#!/bin/bash

project_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
venv_directory="$project_directory/venv"

echo "-----------------------------------------------------------------------------"
echo "|                                Remove venv                                |"
echo "| Author : Alexis EGEA                                                      |"
echo "-----------------------------------------------------------------------------"
echo

echo "Project directory: $project_directory"
echo "Virtual environment path: $venv_directory"
echo

if [ ! -d "$venv_directory" ]; then
  echo "No virtual environment found at: $venv_directory"
  read -p "Press any key to close the terminal window..."
  exit 0
fi

read -p "Do you want to remove this venv? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "Operation cancelled."
  read -p "Press any key to close the terminal window..."
  exit 0
fi

rm -rf "$venv_directory"

if [ -d "$venv_directory" ]; then
  echo "Failed to remove virtual environment."
  read -p "Press any key to close the terminal window..."
  exit 1
fi

echo "Virtual environment removed successfully."
echo
echo "Done!"
read -p "Press any key to close the terminal window..."