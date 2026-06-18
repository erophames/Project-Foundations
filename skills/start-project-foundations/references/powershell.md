# PowerShell Best Practices

Sources:
- Advanced functions: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced
- Comment-based help: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comment_based_help
- Approved verbs: https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands
- PSScriptAnalyzer: https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview
- Module manifests: https://learn.microsoft.com/en-us/powershell/scripting/developer/module/how-to-write-a-powershell-module-manifest
- Pester quick start: https://pester.dev/docs/quick-start

## Use This Reference

Apply this reference when PowerShell owns automation, Windows administration, Azure tooling, cross-platform scripts, modules, DSC helpers, or CI/release orchestration. PowerShell is object-pipeline automation, not Bash with different syntax. Prefer advanced functions, approved verbs, parameter validation, Pester tests, and PSScriptAnalyzer.

Default stance:

- Target PowerShell 7+ for new cross-platform work unless Windows PowerShell compatibility is required.
- Use `.ps1` for scripts, `.psm1` for modules, `.psd1` for module manifests.
- Use approved verb-noun names for public functions.
- Use PSScriptAnalyzer and Pester.
- Keep external process invocation isolated and tested.

## Default Structure

For a script project:

```text
project-name/
|-- scripts/
|   `-- Invoke-ProjectTask.ps1
|-- tests/
|   `-- Invoke-ProjectTask.Tests.ps1
`-- README.md
```

For a module:

```text
ProjectName/
|-- ProjectName.psd1
|-- ProjectName.psm1
|-- Public/
|   `-- Get-ProjectItem.ps1
|-- Private/
|   `-- ConvertTo-ProjectRecord.ps1
|-- tests/
|   `-- Get-ProjectItem.Tests.ps1
`-- README.md
```

Dot-source public/private function files from the module entrypoint when using split files. Export only public functions through the manifest or module file.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Single script | `scripts/Verb-Noun.ps1`, `tests/*.Tests.ps1` | Use parameters and comment help. |
| Module | `.psd1`, `.psm1`, `Public/`, `Private/` | Export narrow public command surface. |
| CI/release automation | `scripts/ci/*.ps1` | Make all inputs explicit; avoid profile dependence. |
| Azure/admin tooling | Module with typed parameters | Support `-WhatIf` for risky changes. |
| Cross-platform tool | PowerShell 7+, path-safe APIs | Avoid Windows-only assumptions unless declared. |

## Naming And Style

- Use approved `Verb-Noun` names for public commands: `Get-`, `Set-`, `New-`, `Remove-`, `Test-`, `Invoke-`.
- Use singular nouns unless the command naturally operates on a collection concept.
- Use PascalCase for function names and parameters.
- Use lowerCamelCase or PascalCase consistently for local variables; prefer clarity over abbreviation.
- Use `[CmdletBinding()]` for advanced functions.
- Use `[Parameter(Mandatory)]`, `[ValidateNotNullOrEmpty()]`, and typed parameters at boundaries.
- Use comment-based help for public scripts/functions.
- Avoid aliases in scripts (`Where-Object`, not `?`; `ForEach-Object`, not `%`).
- Avoid positional parameters in scripts intended for automation.

## API And Function Design

- Prefer pipeline-aware advanced functions for reusable commands.
- Keep `begin`, `process`, and `end` blocks meaningful; do not add them mechanically.
- Return objects, not formatted text, from functions intended for composition.
- Use `Write-Verbose`, `Write-Warning`, and `Write-Error` intentionally; avoid `Write-Host` except for direct console UX.
- Use `SupportsShouldProcess` for commands that change external state.
- Throw terminating errors for failures callers must handle.
- Keep environment and filesystem assumptions explicit.
- Use `Join-Path`, `Resolve-Path`, and platform-safe APIs for paths.

## Tooling Defaults

Recommended commands:

```powershell
Invoke-ScriptAnalyzer -Path . -Recurse
Invoke-Pester
Test-ModuleManifest ./ProjectName.psd1
```

For scripts:

```powershell
pwsh -NoProfile -File ./scripts/Invoke-ProjectTask.ps1 -Help
```

Use `-NoProfile` in CI and tests so user profiles cannot hide missing imports or dependencies.

## Testing And TDD

- Use Pester for unit and behavior tests.
- Start with one failing test for parameter validation, pipeline input, object output, error behavior, or `ShouldProcess`.
- Mock external commands carefully; prefer wrapping external calls in one private function and testing the public function behavior.
- Use temporary drives/directories for filesystem effects.
- Test `-WhatIf` or `ShouldProcess` behavior for destructive commands.
- Test non-Windows path behavior for cross-platform modules.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Static analysis | `Invoke-ScriptAnalyzer -Path . -Recurse` | Finds style, compatibility, and safety issues. |
| Tests | `Invoke-Pester` | Runs Pester tests. |
| Manifest | `Test-ModuleManifest ./ProjectName.psd1` | Validates module metadata. |
| Smoke | `pwsh -NoProfile -File ./scripts/name.ps1 -Help` | Verifies script starts without profiles. |

For published modules, also test import from a clean session and verify exported commands.

## CI Baseline

```powershell
$PSVersionTable
Install-Module PSScriptAnalyzer -Scope CurrentUser -Force
Install-Module Pester -Scope CurrentUser -Force
Invoke-ScriptAnalyzer -Path . -Recurse
Invoke-Pester
```

Pin module versions in serious CI. Run on Windows and Linux when the module claims cross-platform support.

## Security And Robustness

- Do not execute user-provided strings with `Invoke-Expression`.
- Validate paths, URLs, and command arguments before use.
- Prefer splatting with hashtables for command construction.
- Avoid writing secrets to host output, transcripts, or error messages.
- Support `-Confirm` and `-WhatIf` for destructive actions.
- Use `SecureString` only where the platform/API expects it; do not treat it as general encryption.

## Review Hot Spots

- Non-approved verbs and alias-heavy scripts.
- Text output where structured objects are expected.
- Profile-dependent imports or environment variables.
- `Write-Host` used for data flow.
- External process strings with weak quoting.
- Missing `ShouldProcess` on destructive commands.
- Tests that only verify mocks and never inspect object output.
- Module manifests that export everything accidentally.
