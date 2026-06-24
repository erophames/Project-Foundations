# Python Best Practices

Sources:
- PEP 8: https://peps.python.org/pep-0008/
- PyPA `pyproject.toml`: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- PyPA src layout discussion: https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- uv: https://docs.astral.sh/uv/
- Ruff: https://docs.astral.sh/ruff/
- pytest: https://docs.pytest.org/en/stable/getting-started.html
- mypy: https://mypy.readthedocs.io/en/stable/getting_started.html
- Pyright: https://microsoft.github.io/pyright/
- Bandit: https://bandit.readthedocs.io/en/latest/
- pip-audit: https://github.com/pypa/pip-audit
- PyTestArch: https://github.com/sbrunk/pytestarch
- Import Linter: https://import-linter.readthedocs.io/en/latest/
- Vulture: https://github.com/jendrikseipp/vulture
- Radon: https://radon.readthedocs.io/en/latest/
- Coverage.py: https://coverage.readthedocs.io/en/latest/
- Pre-commit: https://pre-commit.com/
- Python `venv`: https://docs.python.org/3/library/venv.html
- Python logging HOWTO: https://docs.python.org/3/howto/logging.html
- Python packaging build frontend: https://build.pypa.io/

## Use This Reference

Apply this reference when the project's primary deliverable is Python source code: a package, CLI, service, script collection, notebook-backed analysis project, automation tool, or library. For framework projects, start with this reference, then layer the selected framework's defaults on top. Do not let a framework template move domain logic into untestable route handlers, notebooks, or command entrypoints.

Use these defaults unless the repo already has a stronger convention:

- Package/library or reusable app: `src/` layout, `pyproject.toml`, pytest, Ruff, type checking.
- Use `uv` as the primary project, dependency, and virtual environment manager. It replaces pip, venv, pip-tools, and virtualenv in a single fast tool.
- Small one-off script: flat layout is acceptable, but still add tests if it will be reused.
- CLI: importable package under `src/`, a thin console entrypoint, behavior tests for command handling.
- Service: `src/package_name/` with domain, adapters, config, and tests separated.
- Notebook project: notebooks are consumers; tested transformation code lives in modules.

Before running Python setup or verification commands, determine the Python interpreter first. Do not assume bare `python` points to the intended Python 3 runtime on every machine.

## Default Structure

Use `src/` layout for packages and reusable applications:

```text
project-name/
├── pyproject.toml
├── README.md
├── src/
│   └── package_name/
│       ├── __init__.py
│       └── module.py
└── tests/
    └── test_module.py
```

Use flat layout only for small scripts that are not packaged. For services, keep framework entrypoints thin and put business logic under `src/package_name/`.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Library | `src/package_name/`, `tests/`, `pyproject.toml` | Keep public API intentional in `__init__.py`; avoid exposing internals accidentally. |
| CLI | `src/package_name/cli.py`, `src/package_name/__main__.py`, `tests/test_cli.py` | Put parsing and execution behind callable functions so tests do not shell out for every case. |
| Web service | `src/package_name/api/`, `src/package_name/domain/`, `src/package_name/adapters/` | Keep route handlers thin; test domain/application services directly. |
| Data pipeline | `src/package_name/transforms/`, `data/raw/`, `data/processed/`, `tests/fixtures/` | Keep data outputs generated and ignored unless they are fixtures. |
| Notebook analysis | `notebooks/`, `src/package_name/`, `tests/` | Keep notebooks reproducible and side-effect-light; move logic into importable modules. |

Avoid creating `utils.py` as the first shared module. Prefer names that describe the responsibility: `email_addresses.py`, `invoice_totals.py`, `postgres_repository.py`.

## Naming And Style

- Follow PEP 8 unless the existing project has a stronger local convention.
- Use `snake_case` for modules, functions, variables, and packages.
- Use `PascalCase` for classes and exceptions; suffix custom exceptions with `Error`.
- Use `UPPER_SNAKE_CASE` for constants.
- Prefer explicit imports and avoid wildcard imports.
- Use type hints on public functions and boundary-heavy internal functions.
- Keep modules focused; split when a module mixes unrelated IO, domain logic, and presentation.

## API And Module Design

- Put public API surface in a small number of modules. Treat exported names as contracts.
- Use leading underscore names for module-private helpers; do not rely on `__all__` alone for clarity.
- Prefer dataclasses or small typed classes for structured data at boundaries.
- Use `pathlib.Path` instead of raw string paths in new code where practical.
- Keep IO at the edges. Domain functions should accept values and return values, not read global files or environment variables.
- Use dependency injection through parameters for clocks, random sources, filesystem roots, clients, and configuration.
- Avoid import-time side effects. Importing a module should not read config, connect to a service, start threads, or parse CLI arguments.
- Use exceptions for exceptional failures, not normal control flow. Define project-specific exceptions only when callers can act on them.
- Use `logging.getLogger(__name__)` in libraries and services. Do not call `basicConfig()` in library code.

## Starter `pyproject.toml`

Use this as the initial shape and tighten it for the actual project:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "package-name"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
  "build",
  "mypy",
  "pyright",
  "pytest",
  "pytest-cov",
  "ruff",
  "bandit",
  "pip-audit",
  "pytestarch",
  "import-linter",
  "vulture",
  "radon",
  "pre-commit",
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.mypy]
python_version = "3.11"
packages = ["package_name"]
strict = true

[tool.pyright]
include = ["src"]
pythonVersion = "3.11"
typeCheckingMode = "strict"

[tool.bandit]
targets = ["src"]

[tool.vulture]
paths = ["src"]

[tool.importlinter]
root_packages = ["package_name"]

[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
fail_under = 80
```

For applications, pin runtime dependencies through the chosen lock workflow (`uv lock`). For libraries, keep dependency ranges compatible and avoid unnecessary upper bounds unless a known break exists.

## Dependency And Environment Policy

- Determine the Python interpreter first:

  ```bash
  python3 --version
  ```

  If `python3` is unavailable, check `python --version`. Use the command that reports the intended supported Python 3 version for all subsequent setup and verification commands. In examples, set `PYTHON=python3` or replace it with the detected executable.
- Use `uv` as the primary environment and dependency manager:

  ```bash
  uv venv
  uv pip install -e ".[dev]"
  uv sync
  ```

  `uv` replaces `python -m venv`, `pip install`, and lock file generation in a single tool. For projects not using `uv`, fall back to `$PYTHON -m venv .venv` + `pip install`.
- Commit lock files for applications, CLIs, services, and reproducible analysis projects.
- Libraries should commit build metadata and test constraints; publishing libraries usually should not require consumers to use the same lock file.
- Add heavy dependencies only when they remove real complexity. A small CLI does not need a full web framework.
- Keep optional integrations behind extras, for example `package-name[postgres]`.
- Pin the minimum supported Python version in `requires-python` and align Ruff/mypy targets with it.

## Quality Gates

| Gate | Default command | Purpose |
| --- | --- | --- |
| Unit tests | `uv run pytest` | Behavior and regression coverage. |
| Coverage | `uv run pytest --cov` | Coverage measurement and threshold enforcement. |
| Format check | `uv run ruff format --check .` | Deterministic formatting. |
| Lint | `uv run ruff check .` | Imports, bugbear-style issues, modernization, simple defects. |
| Types (mypy) | `uv run mypy src` | Public contract and boundary checking. |
| Types (Pyright) | `uv run pyright` | High-performance type checking; catches what mypy misses. |
| Security | `uv run bandit -r src/` | Source code vulnerability scanning. |
| Dependency CVEs | `uv run pip-audit` | Scans installed packages for known security CVEs. |
| Dead code | `uv run vulture src/` | Finds unused/unreachable code. |
| Complexity | `uv run radon cc src/ -s` | Cyclomatic complexity and maintainability metrics. |
| Architecture | `uv run pytest` (PyTestArch + Import Linter) | Layer dependency and import contract enforcement. |
| Build | `uv build` | Confirms package metadata and source inclusion. |

For services, add a smoke test for startup/config parsing. For CLIs, add at least one command invocation test. For data pipelines, add representative fixture tests for empty, null-heavy, duplicate, and malformed inputs.

## Tooling Defaults

Use `pyproject.toml` as the single config home:

- Project/dependency management: `uv` (replaces pip, venv, pip-tools in a single fast tool).
- Build metadata: `[build-system]` and `[project]`.
- Formatting and linting: Ruff formatter and linter (replaces Black, isort, Flake8).
- Type checking: mypy AND Pyright. Run both — Pyright catches issues mypy misses, especially with complex type narrowing and protocol matching.
- Testing: pytest.
- Coverage: Coverage.py via `pytest-cov`.
- Security: Bandit for source code vulnerabilities; pip-audit for dependency CVE scanning.
- Architecture: PyTestArch for layer dependency enforcement; Import Linter for import contract rules.
- Dead code: Vulture for unused code detection.
- Complexity: Radon for cyclomatic complexity and maintainability metrics.
- Git hooks: Pre-commit to orchestrate all tools before every commit.
- Dependency manager: `uv` is the default for new projects. Use `uv lock` for reproducible lock files.

Recommended commands (uv):

```bash
uv run pytest
uv run pytest --cov
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pyright
uv run bandit -r src/
uv run pip-audit
uv run vulture src/
uv run radon cc src/ -s
uv build
```

For projects not using `uv`, replace `uv run` with `$PYTHON -m` and `uv build` with `$PYTHON -m build`.

## CI Baseline

Run checks in this order because failures become easier to interpret:

1. Detect the Python executable and print its version.
2. Install the project with dev dependencies using `uv sync` (or `uv pip install -e ".[dev]"`).
3. Run Ruff format check.
4. Run Ruff lint.
5. Run mypy for packages/services.
6. Run Pyright for packages/services.
7. Run pytest with coverage.
8. Run Bandit security scan.
9. Run pip-audit dependency scan.
10. Run Vulture dead code check.
11. Run Radon complexity report.
12. Run architecture tests (PyTestArch / Import Linter).
13. Run package build for distributable projects.

Do not make CI depend on local environment variables unless the test explicitly documents them. Use temporary directories and fake service clients for unit tests.

## TDD Guidance

- Put tests under `tests/` mirroring source behavior, not implementation files mechanically.
- Name tests by behavior: `test_rejects_empty_email`, not `test_validate_email`.
- Write a failing pytest test first, run only that test, implement the smallest code, then run the full test suite.
- Avoid broad mocking; prefer real objects and temporary files via pytest fixtures.
- For CLI apps, test the command runner separately from `if __name__ == "__main__"`.

## Test Design Details

- Prefer behavior-oriented tests over one-test-per-function mirroring.
- Use `tmp_path`, `monkeypatch`, and `capsys` instead of manually managing temp files and globals.
- Use parametrization for input matrices, but keep the table small enough that failures stay readable.
- Use contract tests for plugin-style interfaces and adapters.
- Use integration tests for database, HTTP, queue, filesystem, and subprocess boundaries.
- Keep slow tests marked, documented, and separated from the default fast loop.
- Avoid snapshot tests for broad Python objects unless the serialized output is the real contract.

## Security And Robustness Defaults

- Validate untrusted input at the boundary with explicit error messages.
- Avoid `eval`, `exec`, unsafe deserialization, shell=True, and dynamic imports from user input.
- Use `subprocess.run([...], check=True)` with argument lists instead of shell strings.
- Use timeouts on network calls.
- Treat path traversal as a real risk for archive extraction, uploads, and file-serving tools.
- Keep secrets out of logs and repr output.
- For services, centralize config parsing and fail fast on missing required settings.
- Run Bandit in every CI build to catch common security anti-patterns (assert usage, hardcoded passwords, weak crypto).
- Run pip-audit to detect known CVEs in installed dependencies; fail the build on high-severity findings.

## Architecture Testing

Use PyTestArch and Import Linter to enforce architectural rules as executable tests:

- **PyTestArch:** assert that modules in `domain/` do not import from `adapters/` or `api/`. Define layer dependency rules as test assertions that fail the build when violated.
- **Import Linter:** define high-level import contracts in `[tool.importlinter]` — for example, forbidding `api` from importing `infrastructure`, or enforcing that `domain` has no external dependencies.
- Both run as part of `pytest` and treat architecture violations as test failures.

## Dead Code And Complexity

- Run Vulture to detect unused functions, variables, imports, and classes that are unreachable.
- Run Radon to calculate cyclomatic complexity (CC) and maintainability index (MI). Set thresholds that flag overly complex functions for refactoring.
- Treat high-complexity and dead-code findings as review items, not necessarily build failures, but track them over time.

## Git Hooks With Pre-commit

Use Pre-commit to orchestrate all quality tools automatically before every commit:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.9
    hooks:
      - id: bandit
        args: [-r, src/]
  - repo: https://github.com/jendrikseipp/vulture
    rev: v2.11
    hooks:
      - id: vulture
```

Keep pre-commit hooks fast (format, lint, type check). Put heavier checks (full test suite, pip-audit, radon) in CI or pre-push stages. Run `pre-commit install` after cloning to activate hooks.

## Planning Checklist

- Add `pyproject.toml` with project metadata, uv, and all tool sections.
- Add `src/package_name/` with a small public boundary.
- Add `tests/` with the first failing behavior test.
- Add Ruff format and lint checks to CI/local verification.
- Add mypy and Pyright type checking.
- Add pytest with Coverage.py reporting.
- Add Bandit and pip-audit security scanning.
- Add Vulture and Radon for dead code and complexity.
- Add PyTestArch and Import Linter for architecture enforcement.
- Add Pre-commit configuration for automated git hooks.
- Run `uv lock` for reproducible dependency resolution.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Putting package code at repo root by default | Use `src/` layout for import/package correctness. |
| Tool configs scattered across setup files | Keep config in `pyproject.toml`. |
| Untyped public APIs | Add annotations where callers depend on contracts. |
| Tests importing private implementation details | Test public behavior unless private logic is the explicit unit boundary. |
| Notebook-first production code | Extract logic into importable modules and keep notebooks as consumers. |
