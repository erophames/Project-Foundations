#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

INSTALL_DIR="$TMP_ROOT/plugins/project-foundations"
MARKETPLACE_PATH="$TMP_ROOT/.agents/plugins/marketplace.json"

"$ROOT_DIR/install.sh" \
  --install-dir "$INSTALL_DIR" \
  --marketplace-path "$MARKETPLACE_PATH" \
  --marketplace-name personal \
  --no-codex-add

test -f "$INSTALL_DIR/.codex-plugin/plugin.json"
test -f "$INSTALL_DIR/.claude-plugin/plugin.json"
test -f "$INSTALL_DIR/skills/start-project-foundations/SKILL.md"
test ! -e "$INSTALL_DIR/skills/start-project-best-practices"

python3 - "$INSTALL_DIR" "$MARKETPLACE_PATH" <<'PY'
import json
import pathlib
import sys

install_dir = pathlib.Path(sys.argv[1])
marketplace_path = pathlib.Path(sys.argv[2])

manifest = json.loads((install_dir / ".codex-plugin" / "plugin.json").read_text())
assert manifest["name"] == "project-foundations", manifest
assert manifest["skills"] == "./skills/", manifest

skill = (install_dir / "skills" / "start-project-foundations" / "SKILL.md").read_text()
assert "name: start-project-foundations" in skill, skill

marketplace = json.loads(marketplace_path.read_text())
assert marketplace["name"] == "personal", marketplace
assert marketplace["interface"]["displayName"] == "Personal", marketplace

entries = [entry for entry in marketplace["plugins"] if entry["name"] == "project-foundations"]
assert len(entries) == 1, marketplace
entry = entries[0]
assert entry["source"] == {"source": "local", "path": "./plugins/project-foundations"}, entry
assert entry["policy"] == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, entry
assert entry["category"] == "Productivity", entry
PY

"$ROOT_DIR/install.sh" \
  --install-dir "$INSTALL_DIR" \
  --marketplace-path "$MARKETPLACE_PATH" \
  --marketplace-name personal \
  --no-codex-add

python3 - "$MARKETPLACE_PATH" <<'PY'
import json
import pathlib
import sys

marketplace = json.loads(pathlib.Path(sys.argv[1]).read_text())
entries = [entry for entry in marketplace["plugins"] if entry["name"] == "project-foundations"]
assert len(entries) == 1, marketplace
PY
