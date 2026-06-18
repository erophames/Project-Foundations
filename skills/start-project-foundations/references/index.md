# Reference Index

Load this file first, then load only the language file needed for the project.

## Current Coverage

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

## Language References

| Language | File | Best first question |
| --- | --- | --- |
| Python | `python.md` | Package/library, CLI, service, notebook, or script? |
| C | `c.md` | Library, CLI, embedded, systems daemon, or mixed C/C++? |
| C++ | `cpp.md` | Library, CLI, GUI, game, embedded, or service? |
| Java | `java.md` | Maven or Gradle, library or application? |
| C# | `csharp.md` | Console, service, web API, class library, desktop, or test project? |
| JavaScript | `javascript.md` | Node library/CLI, browser app, full-stack app, or package? |
| TypeScript | `typescript.md` | Package/library, CLI, Node service, frontend app, or monorepo package? |
| Visual Basic | `visual-basic.md` | VB.NET app/library or legacy migration? |
| SQL | `sql.md` | Schema migrations, analytical/dbt project, app queries, or stored procedures? |
| R | `r.md` | Package, analysis project, Shiny app, or report pipeline? |
| Delphi/Object Pascal | `delphi-object-pascal.md` | Delphi VCL/FMX app, Lazarus/FPC app, package/library, or test project? |
| Kotlin | `kotlin.md` | JVM library/CLI/service, Android app, or Kotlin Multiplatform project? |
| Go | `go.md` | Library package, CLI, service, or multi-module workspace? |
| Rust | `rust.md` | Library crate, binary crate, workspace, embedded/no_std, or FFI boundary? |
| Bash/Shell | `bash-shell.md` | Bash script, POSIX sh script, installer, CI helper, or CLI wrapper? |
| PowerShell | `powershell.md` | Script, module, CI/release automation, Azure/admin tooling, or cross-platform tool? |
| PHP | `php.md` | Composer package, CLI, framework app, WordPress plugin, or legacy modernization? |
| Swift | `swift.md` | Swift package, CLI, Apple app, SwiftUI app, or server-side Swift project? |
| Ruby | `ruby.md` | Gem, CLI, Rails app, background worker, or legacy app? |
| Dart | `dart.md` | Dart package, CLI, Flutter app, Flutter package, or generated-code project? |
| Lua | `lua.md` | Library, Neovim plugin, game script, OpenResty component, or embedded runtime? |
| Scala | `scala.md` | JVM library, service, CLI, Spark/data job, or multi-module sbt build? |
| Elixir | `elixir.md` | Library, OTP app, Phoenix app, Mix task, or umbrella project? |

## Reference Depth Standard

Each language file is expected to be a practical new-project brief, not a short checklist. A complete language reference includes:

- researched source links
- when to use the reference
- default and variant folder structures
- naming and coding style
- API/module design guidance
- dependency/build/tooling policy
- starter config snippets where useful
- testing and TDD guidance
- quality gates and CI baseline commands
- security, robustness, or legacy review hot spots

Keep deep detail in the language files, not in `SKILL.md`, so agents only load the ecosystem they need.

## Project-Type Defaults

Prefer these project structures unless the selected language reference says otherwise:

- **Library:** source package/module plus tests and public API examples.
- **CLI:** source package/module plus testable command runner, not all logic in `main`.
- **Service:** source package/module plus config, adapters, integration tests, and local dev entrypoint.
- **Data/SQL/R:** clear separation between raw inputs, transformation code, tests/checks, and generated artifacts.
- **Legacy modernization:** keep existing layout first; add tooling incrementally and document deviations.

## Superpowers Mapping

- Brainstorming output must name the selected language reference and the chosen defaults.
- Writing plans must include file-level setup and exact verification commands.
- TDD must start with the smallest test for one behavior.
- Verification must include all available checks: format, lint/static analysis, tests, and build/package validation.

## Source Policy

Language files favor official or maintainer documentation. When an ecosystem lacks one official style guide, the file calls that out and uses widely adopted community/project conventions with explicit caveats.
