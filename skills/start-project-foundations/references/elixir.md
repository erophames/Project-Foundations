# Elixir Best Practices

Sources:
- Elixir introduction: https://hexdocs.pm/elixir/introduction.html
- Mix documentation: https://hexdocs.pm/mix/Mix.html
- ExUnit documentation: https://hexdocs.pm/ex_unit/ExUnit.html
- Elixir formatter APIs: https://hexdocs.pm/elixir/Code.html
- Credo overview: https://hexdocs.pm/credo/overview.html
- Dialyxir README: https://hexdocs.pm/dialyxir/readme.html

## Use This Reference

Apply this reference when Elixir owns an OTP application, Phoenix app, library, CLI/mix task, data pipeline, background worker, or distributed system component. Elixir projects should lean on Mix, ExUnit, the formatter, OTP supervision, explicit boundaries, and small processes with clear ownership.

Default stance:

- Use Mix for new projects.
- Use standard `lib/` and `test/` layout.
- Use `mix format`, ExUnit, Credo, and Dialyzer/Dialyxir when useful.
- Model state ownership with processes only when concurrency, isolation, or lifecycle justify it.
- Keep Phoenix contexts or equivalent boundaries meaningful.

## Default Structure

For a library or OTP app:

```text
project_name/
|-- mix.exs
|-- config/
|   `-- config.exs
|-- lib/
|   |-- project_name.ex
|   `-- project_name/
|       `-- worker.ex
|-- test/
|   |-- test_helper.exs
|   `-- project_name_test.exs
`-- README.md
```

For Phoenix, use the generator layout and keep contexts as the main application boundary. Do not put all behavior in controllers, LiveViews, or schemas.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Library | `lib/project_name.ex`, `test/` | Keep public module API documented. |
| OTP app | Application module, supervisors, workers | Supervise long-lived processes deliberately. |
| Phoenix app | Phoenix layout plus contexts | Keep web layer thin and contexts cohesive. |
| Mix task | `lib/mix/tasks/name.ex` | Keep task parsing separate from behavior. |
| Umbrella | `apps/*` | Use only for real deploy/runtime boundaries. |

## Naming And Style

- Use `snake_case` for files, functions, variables, and atoms.
- Use `PascalCase` module names nested under the app namespace.
- Match file paths to modules: `lib/my_app/user_store.ex` defines `MyApp.UserStore`.
- Use `?` suffix for predicates and `!` suffix for functions that raise on failure.
- Prefer pattern matching and function heads for clear branching.
- Keep pipelines readable; break or name intermediate values when transformations become opaque.
- Use module attributes for compile-time constants and docs, not mutable state.
- Use `@moduledoc` and `@doc` for public modules/functions.

## API And OTP Design

- Keep pure functions pure and easy to test.
- Use processes for state ownership, concurrency, backpressure, or lifecycle, not as generic objects.
- Supervise long-lived processes; do not spawn unlinked orphan work.
- Keep GenServer callbacks thin; move business decisions into pure functions where possible.
- Use messages with documented shapes for public process APIs.
- Return `{:ok, value}` / `{:error, reason}` tuples for recoverable failures.
- Use bang functions sparingly for caller-convenience wrappers around safe functions.
- Keep Phoenix contexts focused on a coherent domain capability.

## Mix And Dependency Policy

- Define app metadata, deps, aliases, and preferred CLI envs in `mix.exs`.
- Commit `mix.lock` for applications and services.
- Libraries may commit `mix.lock` for CI reproducibility according to repo convention.
- Keep dependencies small and avoid adding processes/supervision trees implicitly.
- Use runtime config for deployment-specific values; avoid compile-time config for secrets.

Starter aliases:

```elixir
defp aliases do
  [
    test: ["test"],
    check: ["format --check-formatted", "test", "credo --strict"]
  ]
end
```

## Tooling Defaults

Recommended commands:

```bash
mix deps.get
mix format --check-formatted
mix test
mix credo --strict
mix dialyzer
```

Use Dialyzer/Dialyxir for applications with enough type/spec surface to benefit. Do not block tiny prototypes on PLT setup unless the project needs it.

## Testing And TDD

- Put tests under `test/` and name files `*_test.exs`.
- Start with one failing ExUnit test for a pure function, context function, process API, parser, or Mix task behavior.
- Test pure functions before GenServer callback internals.
- Use `setup` blocks for fixture setup and keep them small.
- Use supervised processes in tests where lifecycle matters.
- Test error tuples, invalid input, process crashes/restarts, and timeout behavior.
- Use async tests only when they do not share global/process/database state.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Dependencies | `mix deps.get` | Resolves dependencies. |
| Format | `mix format --check-formatted` | Enforces formatter output. |
| Tests | `mix test` | Runs ExUnit tests. |
| Static review | `mix credo --strict` | Finds style/design issues. |
| Types/specs | `mix dialyzer` | Finds success-typing issues. |

For Phoenix, include database setup/migrations and endpoint/context tests as appropriate.

## CI Baseline

```bash
elixir --version
mix deps.get
mix format --check-formatted
mix test
mix credo --strict
mix dialyzer
```

Cache dependencies and Dialyzer PLTs according to CI platform. Run PostgreSQL or other services explicitly for integration tests.

## Security And Robustness

- Validate external params before passing into contexts.
- Keep atoms from untrusted input bounded; do not create arbitrary atoms from user data.
- Supervise processes and define restart strategies deliberately.
- Avoid logging secrets or full request payloads.
- Use timeouts for external calls and process interactions.
- Treat distributed Erlang exposure as sensitive infrastructure.

## Review Hot Spots

- GenServers used as object wrappers with no concurrency/lifecycle need.
- Business logic trapped inside callbacks, controllers, or LiveViews.
- Unsupervised spawned processes.
- Unsafe atom creation from external strings.
- Async tests sharing database or process state.
- Missing docs/specs on public library APIs.
- Broad umbrella apps without deployment/runtime boundaries.
