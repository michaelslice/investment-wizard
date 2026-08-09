#!/usr/bin/env bash

set -Eeuo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_VENV="$PROJECT_DIR/backend/.venv"
MCP_VENV="$PROJECT_DIR/mcp/.venv"
SKIP_INSTALL=false
SETUP_ONLY=false

for argument in "$@"; do
  case "$argument" in
    --skip-install) SKIP_INSTALL=true ;;
    --setup-only) SETUP_ONLY=true ;;
    -h|--help)
      echo "Usage: ./setup-and-run.sh [--skip-install] [--setup-only]"
      echo "  --skip-install  Start using existing dependencies."
      echo "  --setup-only    Install everything without starting the servers."
      exit 0
      ;;
    *) echo "Unknown argument: $argument" >&2; exit 2 ;;
  esac
done

log() { printf '\033[1;32m[investment-wizard]\033[0m %s\n' "$1"; }
fail() { printf '\033[1;31m[investment-wizard]\033[0m %s\n' "$1" >&2; exit 1; }

command -v python3 >/dev/null 2>&1 || fail "Python 3.11 or newer is required."
command -v npm >/dev/null 2>&1 || fail "Node.js and npm are required (Node 20+ recommended)."

python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 11))' \
  || fail "Python 3.11 or newer is required."

cd "$PROJECT_DIR"

if [[ "$SKIP_INSTALL" == false ]]; then
  log "Creating the FastAPI virtual environment"
  [[ -x "$BACKEND_VENV/bin/python" ]] || python3 -m venv "$BACKEND_VENV"
  log "Installing backend dependencies"
  "$BACKEND_VENV/bin/pip" install -e 'backend[dev]'

  log "Creating the MCP virtual environment"
  [[ -x "$MCP_VENV/bin/python" ]] || python3 -m venv "$MCP_VENV"
  log "Installing MCP dependencies"
  "$MCP_VENV/bin/pip" install -e 'mcp[dev]'

  log "Installing frontend dependencies"
  npm install
fi

if [[ ! -f "$PROJECT_DIR/.env" && ! -f "$PROJECT_DIR/backend/.env" ]]; then
  cp "$PROJECT_DIR/backend/.env.example" "$PROJECT_DIR/.env"
  printf '\033[1;33m[investment-wizard]\033[0m Created .env from backend/.env.example.\n'
  printf '\033[1;33m[investment-wizard]\033[0m Add a valid OPENAI_API_KEY to enable AI Research.\n'
fi

if [[ "$SETUP_ONLY" == true ]]; then
  log "Setup complete"
  exit 0
fi

if command -v lsof >/dev/null 2>&1; then
  lsof -nP -iTCP:8000 -sTCP:LISTEN >/dev/null 2>&1 \
    && fail "Port 8000 is already in use. Stop the existing API and run this script again."
  lsof -nP -iTCP:5173 -sTCP:LISTEN >/dev/null 2>&1 \
    && fail "Port 5173 is already in use. Stop the existing frontend and run this script again."
fi

API_PID=""
WEB_PID=""
cleanup() {
  trap - INT TERM EXIT
  log "Stopping application"
  [[ -n "$WEB_PID" ]] && kill "$WEB_PID" 2>/dev/null || true
  [[ -n "$API_PID" ]] && kill "$API_PID" 2>/dev/null || true
  wait "$WEB_PID" "$API_PID" 2>/dev/null || true
}
trap cleanup INT TERM EXIT

log "Starting FastAPI at http://127.0.0.1:8000"
"$BACKEND_VENV/bin/uvicorn" src.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000 &
API_PID=$!

log "Starting Vite at http://localhost:5173"
npm --workspace frontend run dev -- --host 127.0.0.1 --port 5173 &
WEB_PID=$!

printf '\n\033[1;32minvestment-wizard is starting.\033[0m\n'
printf 'Frontend: \033[4mhttp://localhost:5173\033[0m\n'
printf 'API docs: \033[4mhttp://localhost:8000/docs\033[0m\n'
printf 'Press Ctrl+C to stop both servers.\n\n'

while kill -0 "$API_PID" 2>/dev/null && kill -0 "$WEB_PID" 2>/dev/null; do
  sleep 1
done

fail "One of the application processes stopped unexpectedly."
