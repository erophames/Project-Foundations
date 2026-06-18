#!/usr/bin/env python3
"""Install Project Foundations into a local Codex plugin marketplace."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
from typing import Any


PLUGIN_NAME = "project-foundations"
OLD_PLUGIN_NAME = "best-practice"
DEFAULT_CATEGORY = "Productivity"
DEFAULT_SOURCE_PATH = f"./plugins/{PLUGIN_NAME}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the Project Foundations Codex/Claude plugin locally."
    )
    parser.add_argument(
        "--source-dir",
        default=pathlib.Path(__file__).resolve().parents[1],
        type=pathlib.Path,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--install-dir",
        default=pathlib.Path.home() / "plugins" / PLUGIN_NAME,
        type=pathlib.Path,
        help="Plugin install directory. Default: ~/plugins/project-foundations",
    )
    parser.add_argument(
        "--marketplace-path",
        default=pathlib.Path.home() / ".agents" / "plugins" / "marketplace.json",
        type=pathlib.Path,
        help="Marketplace JSON path. Default: ~/.agents/plugins/marketplace.json",
    )
    parser.add_argument(
        "--marketplace-name",
        default="personal",
        help="Marketplace name to create when marketplace.json is missing. Default: personal",
    )
    parser.add_argument(
        "--no-codex-add",
        action="store_true",
        help="Only copy files and update marketplace.json; do not run codex plugin add.",
    )
    return parser.parse_args()


def read_json(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def write_json(path: pathlib.Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def display_name_for(marketplace_name: str) -> str:
    if marketplace_name == "personal":
        return "Personal"
    return marketplace_name.replace("-", " ").replace("_", " ").title()


def validate_source(source_dir: pathlib.Path) -> None:
    manifest_path = source_dir / ".codex-plugin" / "plugin.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing plugin manifest: {manifest_path}")

    manifest = read_json(manifest_path)
    if manifest.get("name") != PLUGIN_NAME:
        raise ValueError(
            f"{manifest_path} has name {manifest.get('name')!r}; expected {PLUGIN_NAME!r}"
        )

    skill_path = source_dir / "skills" / "start-project-foundations" / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"Missing skill: {skill_path}")


def is_safe_existing_plugin(path: pathlib.Path) -> bool:
    manifest_path = path / ".codex-plugin" / "plugin.json"
    if not manifest_path.exists():
        return False
    try:
        name = read_json(manifest_path).get("name")
    except Exception:
        return False
    return name in {PLUGIN_NAME, OLD_PLUGIN_NAME}


def copy_plugin(source_dir: pathlib.Path, install_dir: pathlib.Path) -> None:
    source_dir = source_dir.resolve()
    install_dir = install_dir.expanduser().resolve()

    if source_dir == install_dir:
        print(f"Using source directory in place: {install_dir}")
        return

    if install_dir.exists():
        if not is_safe_existing_plugin(install_dir):
            raise RuntimeError(
                f"Refusing to replace {install_dir}; it does not look like {PLUGIN_NAME}."
            )
        shutil.rmtree(install_dir)

    install_dir.parent.mkdir(parents=True, exist_ok=True)

    def ignore(_dir: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if name in {".DS_Store", ".git", "__pycache__"} or name.endswith(".pyc")
        }

    shutil.copytree(source_dir, install_dir, ignore=ignore)
    print(f"Installed plugin files: {install_dir}")


def load_or_create_marketplace(path: pathlib.Path, marketplace_name: str) -> dict[str, Any]:
    path = path.expanduser()
    if path.exists():
        data = read_json(path)
    else:
        data = {
            "name": marketplace_name,
            "interface": {"displayName": display_name_for(marketplace_name)},
            "plugins": [],
        }

    data.setdefault("name", marketplace_name)
    interface = data.setdefault("interface", {})
    if not isinstance(interface, dict):
        raise ValueError(f"{path} interface must be a JSON object")
    interface.setdefault("displayName", display_name_for(str(data["name"])))

    plugins = data.setdefault("plugins", [])
    if not isinstance(plugins, list):
        raise ValueError(f"{path} plugins must be a JSON array")

    return data


def update_marketplace(path: pathlib.Path, marketplace_name: str) -> str:
    path = path.expanduser()
    data = load_or_create_marketplace(path, marketplace_name)
    actual_name = str(data["name"])

    entry = {
        "name": PLUGIN_NAME,
        "source": {"source": "local", "path": DEFAULT_SOURCE_PATH},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": DEFAULT_CATEGORY,
    }

    plugins = [item for item in data["plugins"] if item.get("name") != PLUGIN_NAME]
    plugins.append(entry)
    data["plugins"] = plugins
    write_json(path, data)
    print(f"Updated marketplace: {path}")
    return actual_name


def run_codex_add(marketplace_name: str) -> None:
    codex = shutil.which("codex")
    selector = f"{PLUGIN_NAME}@{marketplace_name}"

    if codex is None:
        print(f"Codex CLI not found. To finish later, run: codex plugin add {selector}")
        return

    print(f"Installing in Codex: codex plugin add {selector}")
    subprocess.run([codex, "plugin", "add", selector], check=True)


def main() -> int:
    args = parse_args()
    source_dir = args.source_dir.expanduser().resolve()
    install_dir = args.install_dir.expanduser()
    marketplace_path = args.marketplace_path.expanduser()

    validate_source(source_dir)
    copy_plugin(source_dir, install_dir)
    marketplace_name = update_marketplace(marketplace_path, args.marketplace_name)

    if not args.no_codex_add:
        run_codex_add(marketplace_name)

    print("Start a new Codex thread before using the updated plugin.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"install failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
