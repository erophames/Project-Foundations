# Project Foundations

Project Foundations is a local Codex/Claude-compatible plugin that helps agents start new software projects with language-specific engineering defaults.

It provides one skill, `start-project-foundations`, which overlays project-setup guidance onto the superpowers workflow. It does not replace superpowers; it injects language conventions into brainstorming, planning, TDD, and verification.

## What It Covers

Project Foundations currently covers:

1. Python
2. C
3. C++
4. Java
5. C#
6. JavaScript
7. Visual Basic
8. SQL
9. R
10. Delphi/Object Pascal
11. Kotlin
12. Go
13. Rust
14. TypeScript
15. Bash/Shell
16. PowerShell
17. PHP
18. Swift
19. Ruby
20. Dart
21. Lua
22. Scala
23. Elixir

Each language reference includes project structures, naming/style rules, tooling, starter config snippets, TDD guidance, CI checks, quality gates, and review hot spots.

## Package Layout

```text
project-foundations/
|-- .codex-plugin/plugin.json
|-- .claude-plugin/plugin.json
|-- install.sh
|-- README.md
|-- scripts/install.py
`-- skills/
    `-- start-project-foundations/
        |-- SKILL.md
        |-- agents/openai.yaml
        `-- references/
            |-- index.md
            |-- python.md
            |-- c.md
            |-- cpp.md
            |-- java.md
            |-- csharp.md
            |-- javascript.md
            |-- typescript.md
            |-- visual-basic.md
            |-- sql.md
            |-- kotlin.md
            |-- go.md
            |-- rust.md
            |-- bash-shell.md
            |-- powershell.md
            |-- php.md
            |-- swift.md
            |-- ruby.md
            |-- dart.md
            |-- lua.md
            |-- scala.md
            |-- elixir.md
            |-- r.md
            `-- delphi-object-pascal.md
```

## Install In Codex

From the plugin root, run:

```bash
./install.sh
```

The installer:

- copies the plugin to `~/plugins/project-foundations`
- creates or updates `~/.agents/plugins/marketplace.json`
- adds the `project-foundations` marketplace entry
- runs `codex plugin add project-foundations@personal` when the Codex CLI is available

After installing or updating the plugin, start a new Codex thread so the updated skill metadata and references are loaded.

Useful options:

```bash
./install.sh --no-codex-add
./install.sh --install-dir ~/plugins/project-foundations
./install.sh --marketplace-path ~/.agents/plugins/marketplace.json
./install.sh --marketplace-name personal
```

Use `--no-codex-add` when preparing files for another machine or when you want to run `codex plugin add` manually.

## Manual Codex Install

Codex installs plugins from configured marketplaces. If you do not want to use `install.sh`, create a small local marketplace that points at this plugin.

Example:

```bash
mkdir -p ~/codex-local-marketplace/plugins
cp -R /path/to/project-foundations ~/codex-local-marketplace/plugins/project-foundations
```

Create `~/codex-local-marketplace/marketplace.json`:

```json
{
  "name": "local-project-foundations",
  "interface": {
    "displayName": "Local Project Foundations"
  },
  "plugins": [
    {
      "name": "project-foundations",
      "source": {
        "source": "local",
        "path": "./plugins/project-foundations"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Then register and install:

```bash
codex plugin marketplace add ~/codex-local-marketplace
codex plugin add project-foundations@local-project-foundations
```

## Install As A Standalone Skill

If you do not want to use the plugin wrapper, install only the skill folder.

Codex skill fallback:

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/project-foundations/skills/start-project-foundations ~/.codex/skills/
```

Claude Code skill fallback:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/project-foundations/skills/start-project-foundations ~/.claude/skills/
```

Use the plugin install when possible. The standalone skill install is a compatibility path for environments that do not load local plugin manifests.

## Use It

Invoke it explicitly when starting a project:

```text
Use project-foundations:start-project-foundations for a new Python CLI.
```

or:

```text
Use $start-project-foundations while planning this Java service.
```

Typical prompts:

```text
Start a new C++ library and apply project foundation structure, tests, tooling, and verification.
```

```text
Plan a dbt/SQL project using the project foundations skill and superpowers workflow.
```

```text
Create a new C# worker service and include the language-specific TDD and CI checks.
```

```text
Start a new Go service with module layout, table tests, formatting, vet, and vulnerability checks.
```

```text
Create a Rust library crate with Cargo structure, rustfmt, Clippy, docs, and integration tests.
```

```text
Plan a TypeScript package with strict tsconfig, type checks, linting, tests, and build verification.
```

```text
Create a PowerShell module with approved verbs, PSScriptAnalyzer, Pester tests, and module manifest checks.
```

When active, the skill loads `references/index.md`, selects the relevant language file, and applies that guidance to:

- folder structure
- naming and coding style
- package/build/dependency tooling
- formatter/linter/static analysis setup
- first failing test placement
- verification commands

## Superpowers Integration

This plugin is designed to work with superpowers:

- During brainstorming, it adds language-specific decisions and defaults.
- During planning, it adds exact files, tool config, first tests, and verification commands.
- During TDD, it uses the language's idiomatic test runner and test location.
- During verification, it requires formatter, linter/static analysis, tests, and build/package checks where available.

No hooks are installed by default. Skill invocation and metadata-based discovery are used instead, because language selection is contextual.

## Maintenance

Add or update language reference files when project coverage changes or ecosystem defaults shift.

After edits, validate the package:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/start-project-foundations
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
tests/test-install.sh
```

The validators check skill metadata and plugin manifest shape. They do not replace reviewing the language references for source quality and practical accuracy.
