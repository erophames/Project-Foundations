# Visual Basic Best Practices

Sources:
- Microsoft Visual Basic coding conventions: https://learn.microsoft.com/en-us/dotnet/visual-basic/programming-guide/program-structure/coding-conventions
- Microsoft Visual Basic program structure: https://learn.microsoft.com/en-us/dotnet/visual-basic/programming-guide/program-structure/
- .NET identifier naming rules and conventions: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names
- `dotnet test`: https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test
- `dotnet format`: https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format
- .NET code analysis: https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview
- MSTest: https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-mstest
- .NET project SDK overview: https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview

## Use This Reference

Apply this reference for VB.NET libraries, console apps, WinForms/WPF apps, test projects, and legacy Visual Basic modernization. Treat legacy shape carefully: preserve working project files and designer files, then add tests and tooling around stable behavior.

Default stance:

- Use SDK-style VB.NET projects for new code when possible.
- Preserve existing legacy layout unless migration is explicitly requested.
- Keep `Option Strict On` for new code.
- Use `.editorconfig`, .NET analyzers, and `dotnet format` where supported.
- Extract behavior from UI event handlers into testable classes/modules.

## Default Structure

For VB.NET projects, use the same solution layout as other .NET projects:

```text
ProjectName/
|-- ProjectName.sln
|-- Directory.Build.props
|-- .editorconfig
|-- src/
|   `-- ProjectName/
|       |-- ProjectName.vbproj
|       `-- Feature.vb
`-- tests/
    `-- ProjectName.Tests/
        |-- ProjectName.Tests.vbproj
        `-- FeatureTests.vb
```

For legacy WinForms/WebForms projects, preserve the existing layout first and introduce tests/tooling around stable seams.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| New library | `src/ProjectName/ProjectName.vbproj`, `tests/ProjectName.Tests/` | Use SDK-style project and .NET CLI. |
| Console app | console project plus testable library/module | Keep `Sub Main` small. |
| WinForms/WPF | UI project plus application/domain classes | Do not put business rules in event handlers. |
| Legacy .NET Framework | preserve `.vbproj`, designer files, resource files | Add tests/tooling incrementally. |
| Migration | old project plus new test project or harness | Lock behavior before restructuring. |

Designer-generated files should remain owned by the IDE. Avoid hand-editing generated regions unless there is no alternative.

## Naming And Style

- Use `PascalCase` for namespaces, types, methods, properties, and events.
- Use `camelCase` for local variables and parameters.
- Prefix interfaces with `I`.
- Suffix asynchronous methods with `Async`.
- Avoid Hungarian notation and type-encoded names.
- Use XML documentation for public APIs that are consumed outside the project.
- Keep `Option Strict On` and `Option Infer On` unless a legacy migration requires otherwise.

## Language And API Design

- Use modules for stateless functions only; use classes when behavior has dependencies or state.
- Prefer constructor-injected dependencies for testable services.
- Keep public APIs small and documented when consumed by other projects.
- Use `Async`/`Await` consistently; do not block async operations with `.Result` or `.Wait()`.
- Avoid `On Error Resume Next` in new code. Use structured exception handling.
- Avoid late binding in new code unless interoperating with COM or legacy APIs.
- Prefer `ReadOnly` fields/properties when values do not change.
- Avoid mutable global state in modules.
- Keep validation close to public boundaries.

## Compiler And Analyzer Defaults

Use project settings or `Directory.Build.props`:

```xml
<Project>
  <PropertyGroup>
    <OptionStrict>On</OptionStrict>
    <OptionExplicit>On</OptionExplicit>
    <OptionInfer>On</OptionInfer>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <AnalysisMode>Recommended</AnalysisMode>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  </PropertyGroup>
</Project>
```

For legacy projects, introduce warning-as-error gradually if the existing warning count is high. Do not block modernization on fixing every historical warning in one pass.

## Starter `.editorconfig`

```ini
root = true

[*.vb]
indent_style = space
indent_size = 4
dotnet_sort_system_directives_first = true
dotnet_style_qualification_for_field = false:suggestion
dotnet_style_qualification_for_property = false:suggestion
dotnet_style_qualification_for_method = false:suggestion
dotnet_style_qualification_for_event = false:suggestion
```

Use naming rules if the repo has a consistent field or module naming convention to enforce.

## Tooling Defaults

- Build: .NET SDK and solution files for SDK-style VB.NET projects.
- Formatting: `.editorconfig` plus `dotnet format`.
- Analysis: built-in .NET analyzers.
- Tests: MSTest, xUnit, or NUnit. MSTest is a conservative default for Microsoft-centered VB.NET projects.

Recommended commands:

```bash
dotnet restore
dotnet build --no-restore -warnaserror
dotnet test --no-build
dotnet format --verify-no-changes
```

For legacy projects that cannot use SDK-style tooling, use the existing MSBuild command and add the closest available analyzer/formatter support.

## Quality Gates

| Gate | SDK-style command | Legacy fallback |
| --- | --- | --- |
| Restore | `dotnet restore` | NuGet restore or existing build restore. |
| Build/analyze | `dotnet build --no-restore -warnaserror` | MSBuild solution/project command. |
| Tests | `dotnet test --no-build` | Test runner for MSTest/xUnit/NUnit project. |
| Format | `dotnet format --verify-no-changes` | IDE/team formatter if CLI unsupported. |
| Package/publish | `dotnet pack` or `dotnet publish` | Existing release build command. |

When CLI support is unavailable, document the exact Visual Studio/MSBuild command that proves the project builds.

## TDD Guidance

- Put new tests under `tests/ProjectName.Tests` when possible.
- Start with behavior around a public class/module rather than UI event handlers.
- Extract logic from forms into testable services before writing large UI tests.
- Keep tests named by expected behavior, not implementation method names.
- Use integration tests for database, COM, filesystem, or UI automation boundaries.

## Test Design Details

- Use MSTest, xUnit, or NUnit consistently. MSTest is often easiest in Microsoft-heavy VB.NET teams.
- Add tests around extracted behavior before reshaping legacy UI code.
- Test public methods/classes rather than private implementation details.
- Use temporary files and test doubles for filesystem, registry, COM, and database boundaries.
- Avoid UI automation for business rules; use it only for actual UI behavior.
- For migrations, add characterization tests that capture current behavior before changing it.

## Legacy Modernization Strategy

1. Identify the smallest behavior currently trapped in a form/module.
2. Add a test harness or test project that can exercise that behavior.
3. Extract the behavior into a class/module without changing behavior.
4. Run tests and existing build.
5. Repeat for the next behavior.

Do not reformat or reorganize large legacy files in the same change as behavior edits. That makes review and rollback difficult.

## UI Boundary Rules

- Event handlers should read UI state, call a service, then update UI state.
- Validation rules should live outside controls when reused or business-critical.
- Database calls should not run directly inside form event handlers.
- Long-running work should be asynchronous or backgrounded with clear cancellation/error handling.
- Keep designer-generated code separate from manually written behavior.

## CI Baseline

SDK-style:

```bash
dotnet restore
dotnet build --no-restore -warnaserror
dotnet test --no-build
dotnet format --verify-no-changes
```

Legacy:

```bash
# NuGet restore command for the solution
# MSBuild solution/project command
# test runner command for the test assembly
```

Replace comments with exact commands in the project plan once the legacy toolchain is known.

## Review Hot Spots

- `Option Strict Off` in new files.
- `On Error Resume Next`.
- Late binding outside interop boundaries.
- Business logic in form event handlers.
- Shared mutable module state.
- Generated designer diffs mixed with behavior changes.
- Tests requiring a developer desktop session when logic could be unit-tested.

## Planning Checklist

- Determine whether this is SDK-style VB.NET or legacy Visual Basic.
- Preserve legacy project shape unless migration is explicitly requested.
- Add `.editorconfig` and strict compiler settings where possible.
- Add first failing test with the chosen .NET test framework.
- Add build, test, format, and analyzer checks to verification.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Forcing a legacy app into a new layout immediately | Add tests and tooling incrementally around the current structure. |
| `Option Strict Off` in new code | Keep strict typing enabled. |
| Logic hidden in UI event handlers | Extract behavior into classes/modules that tests can call. |
| Inconsistent naming with C# projects in the same solution | Use .NET naming conventions across languages. |
| Treating VB.NET as unsupported by modern .NET tooling | Use SDK-style projects where practical. |
