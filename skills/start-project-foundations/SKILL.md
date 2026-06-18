---
name: start-project-foundations
description: Use when starting, scaffolding, planning, or restructuring a new software project in Python, C, C++, Java, C#, JavaScript, TypeScript, Visual Basic, SQL, R, Delphi/Object Pascal, Kotlin, Go, Rust, Bash/Shell, PowerShell, PHP, Swift, Ruby, Dart, Lua, Scala, or Elixir; when selecting language-specific folder structure, coding style, naming, tools, linting, formatting, testing, CI, or verification for a project; or when injecting language best practices into superpowers brainstorming, planning, TDD, or verification workflows.
---

# Start Project Foundations

## Core Rule

Use this skill as a language-specific overlay on the active development workflow. Do not replace superpowers skills; inject the selected language's conventions into them.

**REQUIRED COORDINATION:** If any superpowers workflow is active, keep following it. During brainstorming, add language constraints to the design. During writing-plans, add language-specific setup, tests, and verification steps. During TDD, use the language's normal test runner. Before completion, verify with the language's formatter, linter/analyzer, tests, and build command.

## Quick Start

1. Identify the primary language. If ambiguous, ask one concise question.
2. Read `references/index.md`.
3. Read the selected language reference file listed in the index.
4. Apply the reference as constraints for:
   - project layout
   - naming and coding style
   - formatter/linter/analyzer
   - test framework and TDD workflow
   - build/package/dependency tooling
   - verification commands
5. If the project is polyglot, apply one primary language reference and only the secondary references needed for touched files.

## Superpowers Injection

When a user starts a project:

- In `superpowers:brainstorming`, ask language-relevant questions only when the reference leaves a meaningful choice open, such as library vs CLI vs service, Maven vs Gradle, .NET app vs library, Kotlin JVM vs Android vs Multiplatform, Go module vs service, Rust crate vs workspace, TypeScript package vs app, PHP framework vs package, Swift package vs Apple app, or SQL migration vs dbt project.
- In `superpowers:writing-plans`, include exact initial files, tool config files, first failing tests, and verification commands from the language reference.
- In `superpowers:test-driven-development`, write the first failing test in the idiomatic test location and run the smallest test target before implementation.
- In `superpowers:verification-before-completion`, run the formatter/check mode, linter/static analysis, tests, and build/package check that the reference lists.

## Language Selection

Use the supported language routing table below:

| Language request | Reference |
| --- | --- |
| Python, py | `references/python.md` |
| C, C11, C17, C23 | `references/c.md` |
| C++, cpp, cc, cxx | `references/cpp.md` |
| Java, JVM Java | `references/java.md` |
| C#, dotnet, .NET | `references/csharp.md` |
| JavaScript, Node.js, browser JS | `references/javascript.md` |
| TypeScript, TS, TSX | `references/typescript.md` |
| Visual Basic, VB.NET | `references/visual-basic.md` |
| SQL, database project, migrations, dbt | `references/sql.md` |
| R, R package, analysis project | `references/r.md` |
| Delphi, Object Pascal, Pascal | `references/delphi-object-pascal.md` |
| Kotlin, kt, kts, Kotlin/JVM, Kotlin Multiplatform, Android Kotlin | `references/kotlin.md` |
| Go, Golang | `references/go.md` |
| Rust, Cargo crate | `references/rust.md` |
| Bash, shell, sh, zsh scripts | `references/bash-shell.md` |
| PowerShell, pwsh, ps1, psm1 | `references/powershell.md` |
| PHP, Composer, Laravel, Symfony | `references/php.md` |
| Swift, Swift Package Manager, iOS, macOS | `references/swift.md` |
| Ruby, Rails, gem | `references/ruby.md` |
| Dart, Flutter | `references/dart.md` |
| Lua, LuaJIT, Neovim plugin, OpenResty | `references/lua.md` |
| Scala, sbt | `references/scala.md` |
| Elixir, Mix, OTP, Phoenix | `references/elixir.md` |

## Defaults

- Prefer simple, conventional project structure over custom architecture.
- Keep source, tests, configuration, and generated output clearly separated.
- Choose the smallest standard toolchain that provides format, lint/static analysis, tests, and build verification.
- Do not add framework-specific folders until the user chooses the framework.
- Avoid hooks for this plugin by default. Use the namespaced skill command and automatic skill invocation; hooks are too broad for language selection and can surprise new-project workflows.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Applying every language reference | Load only the primary language and touched secondary languages. |
| Treating supported coverage as architecture guidance | Select architecture and tools by project needs, not by the existence of a language reference. |
| Creating custom structure before tool defaults | Start from ecosystem defaults, then deviate only for a clear reason. |
| Replacing superpowers workflow | Keep superpowers gates and add language-specific constraints inside them. |
| Finishing with tests only | Also run formatting/lint/static analysis/build checks where available. |
