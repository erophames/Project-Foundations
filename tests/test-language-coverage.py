#!/usr/bin/env python3
"""Validate language routing and reference coverage for Project Foundations."""

from __future__ import annotations

import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "start-project-foundations" / "SKILL.md"
REFERENCES = ROOT / "skills" / "start-project-foundations" / "references"
README = ROOT / "README.md"


EXPECTED_REFERENCES = {
    "python.md": "Python",
    "c.md": "C",
    "cpp.md": "C++",
    "java.md": "Java",
    "csharp.md": "C#",
    "javascript.md": "JavaScript",
    "visual-basic.md": "Visual Basic",
    "sql.md": "SQL",
    "r.md": "R",
    "delphi-object-pascal.md": "Delphi/Object Pascal",
    "kotlin.md": "Kotlin",
    "go.md": "Go",
    "rust.md": "Rust",
    "typescript.md": "TypeScript",
    "bash-shell.md": "Bash/Shell",
    "powershell.md": "PowerShell",
    "php.md": "PHP",
    "swift.md": "Swift",
    "ruby.md": "Ruby",
    "dart.md": "Dart",
    "lua.md": "Lua",
    "scala.md": "Scala",
    "elixir.md": "Elixir",
}

FORBIDDEN_TEXT = (
    "T" + "IOBE",
    "t" + "iobe",
)


def assert_contains(text: str, needle: str, path: pathlib.Path) -> None:
    if needle not in text:
        raise AssertionError(f"{path} does not contain {needle!r}")


def main() -> int:
    skill_text = SKILL.read_text(encoding="utf-8")
    index_text = (REFERENCES / "index.md").read_text(encoding="utf-8")
    readme_text = README.read_text(encoding="utf-8")
    all_text_files = [SKILL, README, REFERENCES / "index.md"]

    for filename, language in EXPECTED_REFERENCES.items():
        reference = REFERENCES / filename
        if not reference.exists():
            raise AssertionError(f"Missing reference file: {reference}")

        assert_contains(skill_text, language, SKILL)
        assert_contains(index_text, filename, REFERENCES / "index.md")
        all_text_files.append(reference)

    assert_contains(skill_text, "references/kotlin.md", SKILL)
    assert_contains(skill_text, "references/go.md", SKILL)
    assert_contains(skill_text, "references/rust.md", SKILL)
    assert_contains(skill_text, "references/typescript.md", SKILL)
    assert_contains(skill_text, "references/bash-shell.md", SKILL)
    assert_contains(skill_text, "references/powershell.md", SKILL)
    assert_contains(skill_text, "references/php.md", SKILL)
    assert_contains(skill_text, "references/swift.md", SKILL)
    assert_contains(skill_text, "references/ruby.md", SKILL)
    assert_contains(skill_text, "references/dart.md", SKILL)
    assert_contains(skill_text, "references/lua.md", SKILL)
    assert_contains(skill_text, "references/scala.md", SKILL)
    assert_contains(skill_text, "references/elixir.md", SKILL)
    assert_contains(index_text, "Kotlin", REFERENCES / "index.md")
    assert_contains(index_text, "Go", REFERENCES / "index.md")
    assert_contains(index_text, "Rust", REFERENCES / "index.md")
    assert_contains(index_text, "TypeScript", REFERENCES / "index.md")
    assert_contains(index_text, "Bash/Shell", REFERENCES / "index.md")
    assert_contains(index_text, "PowerShell", REFERENCES / "index.md")
    assert_contains(index_text, "PHP", REFERENCES / "index.md")
    assert_contains(index_text, "Swift", REFERENCES / "index.md")
    assert_contains(index_text, "Ruby", REFERENCES / "index.md")
    assert_contains(index_text, "Dart", REFERENCES / "index.md")
    assert_contains(index_text, "Lua", REFERENCES / "index.md")
    assert_contains(index_text, "Scala", REFERENCES / "index.md")
    assert_contains(index_text, "Elixir", REFERENCES / "index.md")
    assert_contains(readme_text, "Kotlin", README)
    assert_contains(readme_text, "Go", README)
    assert_contains(readme_text, "Rust", README)
    assert_contains(readme_text, "TypeScript", README)
    assert_contains(readme_text, "Bash/Shell", README)
    assert_contains(readme_text, "PowerShell", README)
    assert_contains(readme_text, "PHP", README)
    assert_contains(readme_text, "Swift", README)
    assert_contains(readme_text, "Ruby", README)
    assert_contains(readme_text, "Dart", README)
    assert_contains(readme_text, "Lua", README)
    assert_contains(readme_text, "Scala", README)
    assert_contains(readme_text, "Elixir", README)

    python_text = (REFERENCES / "python.md").read_text(encoding="utf-8")
    assert_contains(python_text, "Determine the Python interpreter first", REFERENCES / "python.md")
    assert_contains(python_text, "python3 --version", REFERENCES / "python.md")
    assert_contains(python_text, "PYTHON=python3", REFERENCES / "python.md")

    table_rows = re.findall(r"^\| .*? \| `[^`]+\.md` \|", index_text, flags=re.MULTILINE)
    if len(table_rows) < len(EXPECTED_REFERENCES):
        raise AssertionError("Language reference table is missing expected rows")

    for path in all_text_files:
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                raise AssertionError(f"{path} contains forbidden text {forbidden!r}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
