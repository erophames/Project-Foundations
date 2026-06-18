# Delphi/Object Pascal Best Practices

Sources:
- Castle Game Engine Object Pascal coding conventions: https://castle-engine.io/coding_conventions
- DUnitX: https://github.com/VSoftTechnologies/DUnitX
- DelphiDabbler style notes: https://delphidabbler.com/articles/article-7
- Lazarus packages and projects: https://wiki.freepascal.org/packages
- Embarcadero Delphi documentation: https://docwiki.embarcadero.com/RADStudio/en/Main_Page
- Free Pascal documentation: https://www.freepascal.org/docs.html
- PasDoc: https://pasdoc.github.io/

Official public style guidance for Delphi/Object Pascal is less centralized than for several other ecosystems. Prefer existing project conventions first, then apply the conservative conventions below.

## Use This Reference

Apply this reference for Delphi, Object Pascal, Lazarus/FPC, VCL, FMX, component packages, libraries, and modernization of existing Pascal codebases. Treat IDE/project files as part of the build contract and preserve existing generated/designer files unless the task explicitly includes migration.

Default stance:

- Keep UI/form code thin and move behavior into plain units.
- Use DUnitX for modern Delphi tests and FPCUnit for Lazarus/FPC.
- Keep source, tests, packages, and generated output separate where the toolchain allows.
- Follow existing project conventions first; otherwise use common modern Delphi/Object Pascal conventions.
- Add command-line build/test verification so the project is not IDE-only.

## Default Structure

For new Delphi/FPC projects, keep source, tests, and generated output separate:

```text
ProjectName/
|-- ProjectName.groupproj
|-- src/
|   |-- ProjectName.Core.pas
|   `-- ProjectName.Types.pas
|-- tests/
|   |-- ProjectName.Tests.dpr
|   `-- ProjectName.Core.Tests.pas
|-- packages/
`-- README.md
```

For VCL/FMX applications, keep form files near their units but move non-UI behavior into plain units under `src/`. For Lazarus/FPC, keep `.lpi`/`.lpk` files in conventional project/package locations.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| VCL/FMX app | project files, form units, `src/` behavior units, `tests/` | Keep event handlers thin. |
| Package/component | `packages/`, `src/`, demos, tests | Public component API must be stable and documented. |
| Library | `src/ProjectName.*.pas`, tests | Keep units focused and dependencies explicit. |
| Lazarus/FPC app | `.lpi`, `.lpr`, `src/`, `tests/` | Use FPCUnit and lazbuild where practical. |
| Legacy modernization | preserve layout, add tests/harnesses | Avoid broad file moves before behavior is covered. |

Avoid creating broad `Common`, `Utils`, or `Global` units. Prefer domain names such as `ProjectName.InvoiceTotals`, `ProjectName.CustomerParser`, `ProjectName.FileLocks`.

## Naming And Style

- Use `PascalCase` for units, types, methods, properties, and constants unless the existing project differs.
- Use the conventional prefixes `T` for classes/records, `I` for interfaces, and `E` for exceptions.
- Use `F` for private fields when following Delphi convention.
- Use clear parameter names; `A`-prefixed parameters are acceptable when the project already uses that style.
- Use unit names that describe ownership, for example `ProjectName.Feature`.
- Keep units focused; avoid broad utility units that become dependency magnets.
- Avoid global mutable state except for framework-required registration.

## Unit And API Design

- Keep one main concept per unit when practical.
- Order unit sections consistently: interface uses, public types/constants, implementation uses, implementation details.
- Keep implementation `uses` dependencies out of the interface section unless required by public types.
- Use `strict private` where supported and appropriate.
- Use properties to protect invariants; direct fields are acceptable for simple records.
- Use constructors to establish valid object state.
- Make ownership rules explicit for object references returned from functions or stored in properties.
- Prefer interfaces for polymorphic service boundaries only when they reduce coupling or improve testability.
- Avoid `with`; it obscures resolution and causes fragile edits.
- Keep conditional compilation symbols centralized and documented.

## Memory And Lifetime Rules

- Every owner frees what it creates. Do not free objects owned by callers or frameworks.
- Prefer `try ... finally` around owned resources.
- Use `FreeAndNil` only when nil assignment prevents real later misuse; do not use it as a habit.
- Avoid returning newly allocated objects without clear ownership documentation.
- Treat event/callback references as potentially nil and check with `Assigned`.
- Be explicit about string encoding at IO boundaries.
- Avoid locale-sensitive parsing for persisted or protocol data; use invariant/dot-format helpers where available.

Example ownership pattern:

```pascal
var
  Stream: TFileStream;
begin
  Stream := TFileStream.Create(FileName, fmOpenRead);
  try
    Result := ParseStream(Stream);
  finally
    Stream.Free;
  end;
end;
```

## Tooling Defaults

- Build: Delphi MSBuild for Delphi projects; `lazbuild`/FPC for Lazarus projects.
- Tests: DUnitX for modern Delphi; FPCUnit for Lazarus/FPC projects.
- Formatting: use the team's configured IDE formatter or a committed formatter config if available.
- Static analysis: use available Delphi analyzers such as Pascal Analyzer or DelphiLint when the team has access.

Recommended Delphi commands:

```bash
msbuild ProjectName.groupproj /t:Build /p:Config=Debug
tests/ProjectName.Tests.exe
```

Recommended Lazarus/FPC commands:

```bash
lazbuild ProjectName.lpi
lazbuild tests/ProjectName.Tests.lpi
```

## Quality Gates

| Gate | Delphi | Lazarus/FPC | Purpose |
| --- | --- | --- | --- |
| Build | `msbuild ProjectName.groupproj /t:Build /p:Config=Debug` | `lazbuild ProjectName.lpi` | Command-line build. |
| Tests | run DUnitX test executable | run FPCUnit test project | Behavior/regression coverage. |
| Release build | MSBuild release config | lazbuild release mode | Catches config-specific issues. |
| Formatting | team IDE formatter/config | team formatter/config | Consistent diffs. |
| Static analysis | Pascal Analyzer/DelphiLint if available | FPC warnings/lints | Defect and warning checks. |

If commercial analyzers are unavailable, at minimum compile with the strongest practical warning set and keep warnings visible in CI.

## TDD Guidance

- Put new behavior in non-visual units first, then call it from forms/views.
- Add a DUnitX/FPCUnit test for the unit before implementing behavior.
- Test parsing, validation, and business rules without UI automation.
- Use integration tests for database, COM, filesystem, and platform APIs.
- Keep form tests minimal; prefer presenter/service tests where possible.

## Test Design Details

- Test plain units before UI forms.
- Name test units after the unit under test, for example `ProjectName.Core.Tests.pas`.
- Test constructors, validation, parsing, error paths, and ownership-sensitive behavior.
- Use temporary directories/files for filesystem behavior.
- Use fake interfaces or small test doubles for database/network/COM boundaries.
- Keep UI automation for actual UI behavior, not business rules.
- Add characterization tests before changing legacy behavior.

## VCL/FMX Boundary Rules

- Event handlers should read control state, call a service/presenter, then update controls.
- Form units should not contain database queries, protocol parsing, or complex business rules.
- Long-running work should not block the UI thread.
- Keep resource strings and user-visible text centralized where localization matters.
- Designer files and generated resources should not be mixed with behavior edits unless necessary.

## Legacy Modernization Strategy

1. Build the project from the command line.
2. Add a test project or harness for one stable behavior.
3. Extract behavior from form/global unit into a plain unit.
4. Verify test and existing build.
5. Repeat in small slices.

Avoid massive reformatting during modernization. Preserve diffs that reviewers can understand.

## CI Baseline

Delphi:

```bash
msbuild ProjectName.groupproj /t:Build /p:Config=Debug
msbuild ProjectName.groupproj /t:Build /p:Config=Release
tests/ProjectName.Tests.exe
```

Lazarus/FPC:

```bash
lazbuild ProjectName.lpi
lazbuild tests/ProjectName.Tests.lpi
tests/ProjectName.Tests
```

Replace executable names with the actual project output paths in generated plans.

## Review Hot Spots

- Business logic inside form event handlers.
- Ambiguous ownership of returned objects.
- `with` blocks.
- Global mutable state.
- Conditional compilation spread across many units.
- Locale-sensitive parsing/formatting used for persisted data.
- Generated IDE file noise mixed with hand-written changes.
- Command-line build missing or stale.

## Planning Checklist

- Identify Delphi vs Lazarus/FPC and VCL vs FMX vs package/library.
- Preserve existing IDE/project files if modernizing.
- Add `src/` and `tests/` separation where possible.
- Add first failing DUnitX/FPCUnit test.
- Add build and test commands for the actual compiler/toolchain.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Business logic trapped in forms | Move behavior into plain units and test it. |
| One large global utility unit | Split by domain responsibility. |
| Generated IDE files mixed with source outputs | Keep output directories outside source folders. |
| Ignoring existing project convention | Follow existing style unless it blocks maintainability. |
| No command-line build path | Add MSBuild or lazbuild verification. |
