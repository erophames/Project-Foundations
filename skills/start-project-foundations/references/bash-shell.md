# Bash/Shell Best Practices

Sources:
- GNU Bash reference manual: https://www.gnu.org/software/bash/manual/bash.html
- ShellCheck wiki: https://www.shellcheck.net/wiki/Home
- shfmt manual: https://github.com/mvdan/sh/blob/master/cmd/shfmt/shfmt.1.scd
- bats-core documentation: https://bats-core.readthedocs.io/en/stable/

## Use This Reference

Apply this reference when the project deliverable is a shell script, installer, CI helper, release script, local automation, bootstrapper, or POSIX-compatible command wrapper. Shell is excellent for orchestrating existing programs and fragile for complex data structures. Keep scripts small, explicit, linted, and tested when they affect developer or production workflows.

Default stance:

- Use Bash for non-trivial scripts unless POSIX `sh` portability is required.
- Put reusable scripts under `scripts/` or `tools/`.
- Use ShellCheck and shfmt by default.
- Use bats-core for behavior tests when the script has branching, parsing, or filesystem effects.
- Keep business logic out of shell when a real language would be safer.

## Default Structure

```text
project-name/
|-- scripts/
|   |-- bootstrap.sh
|   `-- release.sh
|-- test/
|   `-- bootstrap.bats
|-- .shellcheckrc
`-- README.md
```

For a shell-heavy tool:

```text
project-name/
|-- bin/
|   `-- project-tool
|-- libexec/
|   |-- project-tool-command
|   `-- project-tool-shared.bash
|-- test/
|   `-- project-tool.bats
`-- Makefile
```

Keep executable entrypoints in `bin/` and shared helper code in `libexec/` or `scripts/lib/`. Avoid sourcing files from unpredictable relative paths; resolve paths from `${BASH_SOURCE[0]}`.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| One script | `scripts/name.sh` plus README usage | Keep options minimal and failure behavior clear. |
| Installer/bootstrapper | `install.sh`, `scripts/install-*` | Detect prerequisites and print actionable failures. |
| CI helper | `scripts/ci/*.sh` | Avoid relying on interactive shell config. |
| CLI wrapper | `bin/name`, `libexec/` commands | Keep parsing and dispatch predictable. |
| POSIX script | `#!/bin/sh`, no Bash arrays/features | Test under the target shells. |

## Naming And Style

- Use lowercase file names with hyphens for commands: `build-release.sh`.
- Use `snake_case` for functions and local variables.
- Use `UPPER_SNAKE_CASE` for environment variables exported to subprocesses.
- Use long option names in scripts intended for humans: `--install-dir`.
- Use `main "$@"` at the bottom for scripts with functions.
- Use `local` inside Bash functions.
- Prefer `printf` over `echo` for controlled output.
- Quote expansions unless deliberate word splitting is required.
- Use arrays in Bash when passing argument lists.
- Use `[[ ... ]]` for Bash conditionals; use `[ ... ]` only for POSIX scripts.

## Safety Defaults

- Start Bash scripts with:

  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  ```

- Add `IFS=$'\n\t'` only when you understand how it affects reads and splitting.
- Use traps for cleanup:

  ```bash
  tmp_dir="$(mktemp -d)"
  cleanup() { rm -rf "$tmp_dir"; }
  trap cleanup EXIT
  ```

- Never parse `ls`.
- Never build commands with string concatenation when arrays can hold arguments.
- Use `command -v tool >/dev/null 2>&1` for dependency checks.
- Avoid `eval`; if it appears, treat it as a design failure until proven otherwise.
- Be explicit about destructive operations and paths.

## API And UX Design

- Provide `usage()` output for scripts with options.
- Keep stdout for machine-readable or primary output; put logs/status/errors on stderr.
- Use stable exit codes: `0` success, nonzero failure.
- Validate required environment variables at startup.
- Support `--help` and avoid requiring interactive input for automation.
- Make dry-run mode available for risky file, git, deployment, or package operations.
- Prefer idempotent behavior for bootstrappers and CI helpers.

## Tooling Defaults

Recommended commands:

```bash
shellcheck scripts/*.sh
shfmt -w scripts
shfmt -d scripts
bats test
```

For POSIX scripts:

```bash
shellcheck -s sh scripts/*.sh
```

Use a `.shellcheckrc` only for project-wide justified exclusions. Inline disables must be narrow and explain why the rule is wrong for that line.

## Testing And TDD

- Use bats-core for scripts with branches, file output, command dispatch, or error behavior.
- Start with one failing behavior: missing argument, happy path, failure cleanup, option parsing, or dependency detection.
- Use temporary directories for filesystem tests.
- Stub external commands by prepending a temporary directory to `PATH`.
- Test stderr/stdout separately when scripts are used by automation.
- Test failure paths, not only the happy path.
- For destructive scripts, test dry-run behavior first.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Static analysis | `shellcheck scripts/*.sh` | Finds quoting, portability, and logic issues. |
| Format check | `shfmt -d scripts` | Confirms deterministic style. |
| Tests | `bats test` | Runs behavior tests. |
| Smoke | `scripts/name.sh --help` | Confirms script starts and usage works. |

For CI scripts, run them in the same shell used by CI. For installers, test at least one clean temporary install path.

## CI Baseline

```bash
bash --version
shellcheck scripts/*.sh
shfmt -d scripts
bats test
```

Install ShellCheck, shfmt, and bats through the CI platform's package manager or pinned tool actions. Do not depend on user shell startup files such as `.bashrc`.

## Review Hot Spots

- Unquoted expansions, globs, and word splitting.
- `rm -rf` with weak path validation.
- `curl | bash` patterns without checksum or review path.
- Scripts that work only from one current working directory.
- Hidden dependencies on aliases, shell options, or interactive prompts.
- Swallowed errors inside pipelines.
- `eval`, command strings, and unvalidated user input.
- CI scripts that pass locally but not in a clean shell.
