#!/bin/bash

project_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
venv_directory="$project_directory/venv"

echo "-----------------------------------------------------------------------------"
echo "|                         Remove Environment (venv)                         |"
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

# Detect whether the current terminal is using this project venv.
was_active_project_venv=false
if [ -n "$VIRTUAL_ENV" ]; then
  current_venv="$VIRTUAL_ENV"
  project_venv="$venv_directory"

  # Normalize paths on Git Bash / Windows to compare reliably.
  if command -v cygpath >/dev/null 2>&1; then
    current_venv="$(cygpath -m "$VIRTUAL_ENV" 2>/dev/null || echo "$VIRTUAL_ENV")"
    project_venv="$(cygpath -m "$venv_directory" 2>/dev/null || echo "$venv_directory")"
  fi

  if [ "${current_venv,,}" = "${project_venv,,}" ]; then
    was_active_project_venv=true
    echo "Active project venv detected in your terminal."
    echo "Note: this script runs in a child shell and cannot deactivate the parent shell."
  fi
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
if [ "$was_active_project_venv" = true ]; then
  echo "Run 'deactivate' in your current terminal (or reopen it)."
  deactivate
fi
echo
echo "Done!"
read -p "Press any key to close the terminal window..."