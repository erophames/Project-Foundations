# C# Best Practices

Sources:
- Microsoft C# coding conventions: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
- Microsoft identifier naming rules and conventions: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names
- .NET project SDK overview: https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview
- `dotnet test`: https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test
- `dotnet format`: https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format
- .NET code analysis: https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview
- .NET nullable reference types: https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references
- .NET testing overview: https://learn.microsoft.com/en-us/dotnet/core/testing/
- Roslyn Quality Analyzers (CA rules): https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/
- SonarAnalyzer.CSharp: https://github.com/SonarSource/sonar-dotnet
- Meziantou.Analyzer: https://github.com/meziantou/Meziantou.Analyzer
- StyleCop.Analyzers: https://github.com/DotNetAnalyzers/StyleCopAnalyzers
- Microsoft.CodeAnalysis.NetAnalyzers: https://github.com/dotnet/roslyn-analyzers
- NetArchTest: https://github.com/BenMorris/NetArchTest
- PublicApiGenerator: https://github.com/PublicApiGenerator/PublicApiGenerator
- NuGet auditing: https://learn.microsoft.com/en-us/nuget/concepts/auditing-packages
- dotnet-project-licenses: https://github.com/tomchav/dotnet-project-licenses
- Husky.Net: https://alirezanet.github.io/Husky.Net/

## Use This Reference

Apply this reference for C# libraries, CLIs, ASP.NET services, worker services, desktop apps, test projects, and shared .NET solution work. Use the .NET SDK project system and keep project count low until there is a real deployment, ownership, or dependency boundary.

Default stance:

- Use SDK-style projects.
- Put source under `src/` and tests under `tests/`.
- Enable nullable reference types for new code.
- Use `.editorconfig` to make formatting and analyzer expectations executable.
- Enable `TreatWarningsAsErrors` and a mandatory analyzer suite: Roslyn CA rules, Microsoft.CodeAnalysis.NetAnalyzers, SonarAnalyzer.CSharp, Meziantou.Analyzer, and StyleCop.Analyzers.
- Use `dotnet` CLI commands as the local/CI contract.
- Use NetArchTest for executable architecture rule enforcement.
- Use NuGet audit and dotnet-project-licenses for dependency vulnerability and license scanning.
- Use Husky.Net to run all checks automatically before every git commit.

## Default Structure

Use a solution with separate source and test projects:

```text
ProjectName/
|-- ProjectName.sln
|-- Directory.Build.props
|-- .editorconfig
|-- src/
|   `-- ProjectName/
|       |-- ProjectName.csproj
|       `-- Feature.cs
`-- tests/
    `-- ProjectName.Tests/
        |-- ProjectName.Tests.csproj
        `-- FeatureTests.cs
```

Use SDK-style projects. Keep shared build settings in `Directory.Build.props` only when they apply broadly.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Class library | `src/ProjectName/`, `tests/ProjectName.Tests/` | Keep public API intentional and documented. |
| Console/CLI | `src/ProjectName.Cli/`, library project for behavior | Keep `Program.cs` thin; test command behavior separately. |
| ASP.NET API | `src/ProjectName.Api/`, optional application/domain projects | Keep controllers/minimal endpoints thin. |
| Worker service | `src/ProjectName.Worker/`, domain/application code | Keep background loop separate from work unit logic. |
| Desktop | UI project plus testable application/domain library | Keep UI event handlers small. |

Do not split into `Domain`, `Application`, `Infrastructure`, and `Api` projects automatically. Add projects when they enforce real dependency direction or deployment boundaries.

## Naming And Style

- Use `PascalCase` for namespaces, types, methods, properties, events, and public fields.
- Use `camelCase` for local variables and parameters.
- Use `_camelCase` for private fields if the project has no existing field convention.
- Prefix interfaces with `I`.
- Suffix asynchronous methods with `Async`.
- Use meaningful nullable annotations; do not suppress nullability warnings casually.
- Prefer expression-bodied members only when readability improves.
- Keep records and immutable types for values; use classes for identity and behavior.

## API And Type Design

- Prefer records for immutable value-like data and classes for identity/behavior.
- Use `required` properties or constructors to prevent partially initialized objects.
- Use nullable annotations as real contracts. `string?` means callers must handle absence.
- Prefer `IReadOnlyList<T>`/`IReadOnlyCollection<T>` for read-only public collections.
- Do not expose mutable collections directly from public APIs.
- Use `CancellationToken` on async operations that may block or call IO.
- Keep async all the way through IO paths; avoid `.Result` and `.Wait()`.
- Suffix asynchronous methods with `Async`.
- Use dependency injection at application boundaries, not as a substitute for clear constructors in domain code.
- Keep extension methods focused and discoverable; avoid broad `Extensions.cs` files.

## Starter `Directory.Build.props`

Enable `TreatWarningsAsErrors` and reference all mandatory analyzer packages:

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <AnalysisMode>AllEnabledByDefault</AnalysisMode>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    <NuGetAudit>true</NuGetAudit>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.CodeAnalysis.NetAnalyzers" Version="9.0.0" />
    <PackageReference Include="SonarAnalyzer.CSharp" Version="9.32.0.97167" />
    <PackageReference Include="Meziantou.Analyzer" Version="2.0.163" />
    <PackageReference Include="StyleCop.Analyzers" Version="1.2.0-beta.556" />
  </ItemGroup>
</Project>
```

Adjust `TargetFramework` to the runtime/deployment target. Use LTS or the organization's standard target when available. Pin analyzer versions centrally via `Directory.Build.props` so all projects enforce the same rule set.

## Starter `.editorconfig`

```ini
root = true

[*.cs]
indent_style = space
indent_size = 4
dotnet_sort_system_directives_first = true
dotnet_style_qualification_for_field = false:suggestion
dotnet_style_qualification_for_property = false:suggestion
dotnet_style_qualification_for_method = false:suggestion
dotnet_style_qualification_for_event = false:suggestion

dotnet_naming_rule.private_fields_should_be_camel_case.severity = suggestion
dotnet_naming_rule.private_fields_should_be_camel_case.symbols = private_fields
dotnet_naming_rule.private_fields_should_be_camel_case.style = private_field_style

dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private

dotnet_naming_style.private_field_style.capitalization = camel_case
dotnet_naming_style.private_field_style.required_prefix = _
```

Keep analyzer severity strict enough to be useful, but do not enable noisy rules that the team will ignore.

## Tooling Defaults

- Build: .NET SDK and solution files.
- Formatting: `.editorconfig` plus `dotnet format`.
- Analysis — mandatory analyzer suite (all enforced as errors via `TreatWarningsAsErrors`):
  - **Roslyn CA rules**: built-in .NET quality analyzers (CAxxxx), enabled at `AllEnabledByDefault`.
  - **Microsoft.CodeAnalysis.NetAnalyzers**: security, performance, and correctness rules from the Roslyn team.
  - **SonarAnalyzer.CSharp**: code quality, security hotspot, and bug detection from SonarSource.
  - **Meziantou.Analyzer**: best-practice and performance rules covering edge cases the others miss.
  - **StyleCop.Analyzers**: style and documentation enforcement (SAxxxx rules).
- Architecture testing: NetArchTest for enforcing layering, dependency direction, and naming rules through fluent assertions.
- API surface: PublicApiGenerator for snapshot-testing the public API to detect unintentional breaking changes.
- Tests: xUnit, NUnit, or MSTest. xUnit is a conservative default for new libraries; MSTest is fine for Microsoft-heavy teams.
- Coverage: Coverlet when coverage data is needed.
- Security: NuGet audit (built-in, `<NuGetAudit>true</NuGetAudit>`) for transitive package vulnerability scanning.
- License compliance: dotnet-project-licenses for enumerating and verifying dependency licenses.
- Git hooks: Husky.Net to run all checks automatically before every commit.

Recommended commands:

```bash
dotnet restore
dotnet build --no-restore -warnaserror
dotnet test --no-build
dotnet format --verify-no-changes
```

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Restore | `dotnet restore` | Dependency resolution and NuGet audit. |
| Build/analyze | `dotnet build --no-restore -warnaserror` | Compilation, nullable, all 5 analyzer suites. |
| Tests | `dotnet test --no-build` | Behavior and regression coverage. |
| Architecture | NetArchTest suite (runs within `dotnet test`) | Layer, dependency direction, and naming enforcement. |
| API surface | PublicApiGenerator (runs within `dotnet test`) | Detects unintentional public API changes. |
| Format | `dotnet format --verify-no-changes` | `.editorconfig` and formatting enforcement. |
| License scan | `dotnet-project-licenses` | Enumerate and verify dependency licenses. |
| Pack | `dotnet pack --no-build` | Libraries/packages only. |

For ASP.NET APIs, add at least one application factory/integration smoke test. For CLIs, test exit code and console output.

## TDD Guidance

- Put tests in `tests/ProjectName.Tests`.
- Name test classes after the behavior owner: `OrderCalculatorTests`.
- Use clear behavior names, for example `Rejects_negative_quantity`.
- Test public behavior before internals; use `InternalsVisibleTo` sparingly.
- Keep ASP.NET controllers/endpoints thin and test application services directly.

## Test Design Details

- Use xUnit, NUnit, or MSTest consistently across the solution.
- Name test projects `ProjectName.Tests`.
- Name test files after the behavior owner: `OrderCalculatorTests.cs`.
- Prefer real domain objects over mocks. Mock external boundaries: HTTP clients, clocks, queues, filesystems, databases.
- Use `TimeProvider` or a small clock abstraction for time-sensitive code.
- Use `IAsyncLifetime`/fixture patterns sparingly and only when setup is expensive.
- Keep integration tests separate from unit tests if they need database, network, containers, or environment configuration.
- Test nullable and validation behavior explicitly at public boundaries.

## ASP.NET And Service Boundaries

- Controllers/minimal API handlers map transport input/output only.
- Application services own use-case orchestration.
- Domain types enforce invariants without ASP.NET dependencies.
- Persistence adapters implement repository/query interfaces where an abstraction buys testability or portability.
- Configuration binding is centralized and validated at startup.
- Background services delegate one unit of work to a testable class; the loop itself stays small.

## Dependency Policy

- Prefer built-in .NET libraries before adding packages.
- Add package references at the narrowest project that needs them.
- Use central package management when multiple projects need shared version governance.
- Keep test helper packages in test projects only.
- Avoid global service locators and static mutable singletons.
- Enable NuGet audit and review vulnerability reports on every restore.
- Run dotnet-project-licenses to verify license compliance before merging new dependencies.

## CI Baseline

```bash
dotnet --info
dotnet restore
dotnet build --no-restore -warnaserror
dotnet test --no-build
dotnet format --verify-no-changes
dotnet-project-licenses -i ProjectName.sln -o license-report.html
```

For package projects, add `dotnet pack --no-build`. For apps, add a publish or container build check when deployment depends on it. NuGet audit runs automatically during `dotnet restore` when `<NuGetAudit>true</NuGetAudit>` is set.

## Architecture Testing

Use NetArchTest to enforce architectural rules as fluent assertions that fail the build when violated:

- **Layer dependencies:** domain types must not depend on infrastructure or ASP.NET types.
- **Dependency direction:** domain projects must not reference data/access projects.
- **Naming conventions:** controllers must end in `Controller`, services in `Service`.
- **Framework isolation:** domain classes must not inherit from `ControllerBase`, `DbContext`, or other framework base classes.

NetArchTest assertions live in the test project and run as part of `dotnet test`. Treat architecture violations as build failures, not warnings.

## API Surface Verification

Use PublicApiGenerator to snapshot the public API surface and detect unintentional breaking changes:

- Generate the public API on every build and compare against the committed baseline.
- Fail the build when the public API changes without an intentional baseline update.
- This catches accidental visibility changes, removed types, and modified signatures before they ship.

## Security And License Compliance

- Enable NuGet auditing (`<NuGetAudit>true</NuGetAudit>`) for automatic transitive vulnerability scanning during restore.
- Run dotnet-project-licenses in CI to enumerate all dependency licenses and verify compliance with the project's license policy.
- Treat known-vulnerable packages as build failures, not warnings.
- Review the license report for copyleft or restrictive licenses before adding new dependencies.

## Git Hooks With Husky.Net

Use Husky.Net to automate quality checks before code enters the repository:

- Install Husky.Net to run checks on `pre-commit` (format, lint) and `pre-push` (tests, architecture, security).
- Keep pre-commit hooks fast (format check, analyzer diagnostics) so the developer loop stays responsive.
- Put heavier checks (full test suite, license scan, NuGet audit) in `pre-push` or CI only.
- Document the hook setup in the README so new contributors install it on first clone.

## Review Hot Spots

- Nullability suppressions (`!`) without a clear invariant.
- Async-over-sync or sync-over-async deadlock risks.
- Business logic in controllers, Razor pages, forms, or hosted-service loops.
- Public mutable collections.
- Catching broad `Exception` and returning vague failures.
- Tests that only verify mocks were called.
- Over-splitting projects before boundaries exist.

## Planning Checklist

- Create solution, source project, and test project.
- Enable nullable reference types.
- Add `.editorconfig` for naming and analyzer severity.
- Add mandatory analyzer suite to `Directory.Build.props`: NetAnalyzers, SonarAnalyzer.CSharp, Meziantou.Analyzer, StyleCop.Analyzers.
- Set `AnalysisMode=AllEnabledByDefault` and `TreatWarningsAsErrors=true`.
- Enable NuGet audit (`<NuGetAudit>true</NuGetAudit>`).
- Add first failing test in the selected test framework.
- Add NetArchTest assertions for layer and dependency direction rules.
- Add PublicApiGenerator for public API surface verification.
- Add dotnet-project-licenses to CI for license compliance.
- Install Husky.Net for automated pre-commit and pre-push hooks.
- Add build, test, format, and analyzer checks to verification.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Business logic in controllers or UI forms | Move behavior into testable services/domain types. |
| Nullable warnings ignored | Treat nullability as part of the contract. |
| One huge solution project | Split source and tests at minimum; add more projects only for real boundaries. |
| Formatting only through IDE settings | Commit `.editorconfig` and verify with `dotnet format`. |
| Over-mocking simple collaborators | Prefer real domain objects and mock only external boundaries. |
