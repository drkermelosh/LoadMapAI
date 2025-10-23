#!/usr/bin/env bash
set -e

mkdir -p .vscode

# launch.json: Run with F5
cat > .vscode/launch.json << 'EOF'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI (Uvicorn)",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}",
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  ]
}
EOF

# settings.json: format on save; let VS Code discover the venv
cat > .vscode/settings.json << 'EOF'
{
  "editor.formatOnSave": true,
  "python.analysis.typeCheckingMode": "basic",

  // Choose ONE formatter you actually use:
  // If you use Ruff:
  // "editor.defaultFormatter": "charliermarsh.ruff",
  // If you use Black:
  // "editor.defaultFormatter": "ms-python.black-formatter",

  // VS Code will auto-detect .venv; if not, use Command Palette:
  // "Python: Select Interpreter" and pick ./.venv
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true
  }
}
EOF

# tasks.json: quick “Run API” task (Terminal → Run Task…)
cat > .vscode/tasks.json << 'EOF'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run API",
      "type": "shell",
      "command": "uvicorn app.main:app --reload",
      "problemMatcher": []
    }
  ]
}
EOF

echo "✅ VS Code configs written to .vscode/"
echo "Next:"
echo "  1) In VS Code: Cmd+Shift+P → Python: Select Interpreter → choose ./.venv"
echo "  2) Press F5 to run, or Terminal → Run Task… → Run API"
