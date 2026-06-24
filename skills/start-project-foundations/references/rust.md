# Rust Best Practices

Sources:
- Cargo package layout: https://doc.rust-lang.org/cargo/guide/project-layout.html
- Rust API Guidelines naming: https://rust-lang.github.io/api-guidelines/naming.html
- Rustfmt: https://rust-lang.github.io/rustfmt/
- Writing automated tests: https://doc.rust-lang.org/book/ch11-00-testing.html
- Cargo workspaces: https://doc.rust-lang.org/cargo/reference/workspaces.html
- Cargo features: https://doc.rust-lang.org/cargo/reference/features.html
- Clippy: https://doc.rust-lang.org/clippy/
- rustdoc: https://doc.rust-lang.org/rustdoc/
- RustSec Advisory Database: https://rustsec.org/
- cargo-deny: https://github.com/EmbarkStudios/cargo-deny
- cargo-audit: https://github.com/rustsec/rustsec/tree/main/cargo-audit
- cargo-tarpaulin: https://github.com/xd009642/tarpaulin
- cargo-machete: https://github.com/bnjbvr/cargo-machete
- cargo-semver-checks: https://github.com/obi1kenobi/cargo-semver-checks
- cargo-mutants: https://github.com/sourcefrog/cargo-mutants
- cargo-geiger: https://github.com/rust-secure-code/cargo-geiger
- Miri: https://github.com/rust-lang/miri
- Cargo Nextest: https://nexte.st/
- Rust-analyzer: https://rust-analyzer.github.io/

## Use This Reference

Apply this reference when Rust owns the main deliverable: a library crate, binary crate, CLI, service, embedded component, WebAssembly module, FFI boundary, or multi-crate workspace. Rust projects should start from Cargo's defaults, make ownership and error contracts explicit, keep unsafe code isolated, and verify with rustfmt, Clippy, tests, docs, and dependency checks.

Default stance:

- Use Cargo for all new projects.
- Start with a single crate unless separate crates have a clear ownership, compile-time, or publication reason.
- Prefer `src/lib.rs` for testable logic and keep binaries thin.
- Run rustfmt and Clippy in every CI build as mandatory gates.
- Use `Result` and `Option` deliberately instead of panics for expected failure.
- Avoid `unsafe` by default; when needed, isolate and document invariants, and verify with Miri.
- Run cargo-deny and cargo-audit for dependency security, license, and policy enforcement.
- Use Cargo Nextest as the primary test runner for faster, more reliable test execution.
- Run cargo-tarpaulin for coverage measurement.
- Use cargo-machete to detect unused dependencies.
- Run cargo-semver-checks for libraries to prevent accidental breaking API changes.
- Run cargo-mutants for mutation testing to verify test quality.
- Run cargo-geiger to scan the dependency graph for `unsafe` code.
- Use rust-analyzer as the IDE LSP for real-time quality feedback.

## Default Structure

For a library crate:

```text
project-name/
|-- Cargo.toml
|-- README.md
|-- src/
|   `-- lib.rs
|-- tests/
|   `-- integration_test.rs
|-- examples/
|   `-- basic.rs
`-- benches/
```

For an application with a binary and reusable logic:

```text
project-name/
|-- Cargo.toml
|-- README.md
|-- src/
|   |-- main.rs
|   |-- lib.rs
|   `-- config.rs
|-- tests/
|   `-- cli_test.rs
`-- examples/
```

For multiple binaries:

```text
src/
|-- lib.rs
`-- bin/
    |-- import.rs
    `-- serve.rs
```

Use `src/main.rs` for one binary. Use `src/bin/name.rs` for multiple executables. Put integration tests in `tests/`, examples in `examples/`, benchmarks in `benches/`, and module unit tests near the code they exercise.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Library crate | `src/lib.rs`, integration tests, examples | Keep public API small, documented, and semver-aware. |
| Binary crate | `src/main.rs` plus `src/lib.rs` for logic | Keep `main` limited to parsing, setup, and exit handling. |
| CLI | `src/lib.rs`, command parser module, integration tests | Test command behavior without spawning a process for every case. |
| Service | crate modules for config, domain, adapters, transport | Keep framework types at boundaries and domain logic framework-light. |
| Workspace | root `Cargo.toml` with `members`, crates under `crates/` | Use when crates have real independent boundaries. |
| Embedded/no_std | `#![no_std]`, hardware abstraction boundaries | Keep platform-specific code isolated and test pure logic on host where possible. |
| FFI | `ffi` module/crate, explicit C ABI surface | Contain unsafe, validate pointers, and document ownership rules. |

Do not split into many crates at project start just to mirror architecture diagrams. A module inside one crate is cheaper until compile times, ownership, publication, or dependency boundaries justify a workspace.

## Naming And Style

- Use `snake_case` for local variables, functions, methods, modules, and file names.
- Use `UpperCamelCase` for types, traits, enum variants, and type parameters.
- Use `SCREAMING_SNAKE_CASE` for constants and statics.
- Use concise crate names. Package names in `Cargo.toml` often use kebab-case; the imported crate name uses underscores.
- Name traits by capability: `Read`, `Serialize`, `Repository`, `Clock`. Avoid vague `Manager` and `Helper` suffixes.
- Use rustfmt's output as the formatting authority.
- Keep modules focused and named after domain concepts, not buckets like `utils`.
- Prefer explicit visibility. Start private, then expose `pub`, `pub(crate)`, or `pub(super)` only when needed.
- Keep `use` imports clear and local to the module that needs them.
- Add rustdoc comments for public crates, modules, types, traits, functions, and tricky invariants.

## API And Module Design

- Model ownership at the API boundary. Decide whether callers pass owned values, borrows, mutable borrows, `Arc`, or iterators.
- Prefer borrowing in APIs when the callee does not need ownership.
- Return owned values when that makes lifetime use simpler for callers and cost is acceptable.
- Use `Result<T, E>` for recoverable failures and `Option<T>` for absence.
- Avoid `unwrap` and `expect` in library code except for impossible invariants with clear messages.
- For applications, `anyhow` is acceptable at top-level orchestration boundaries. For libraries, prefer typed errors with `thiserror` or manual error enums.
- Keep error enums non-exhaustive or carefully versioned if they are public.
- Use newtypes to prevent mixing domain values such as IDs, amounts, paths, or units.
- Use builders for configuration that has many optional fields or validation.
- Prefer iterators and slices at API boundaries when they reduce allocation without obscuring behavior.
- Avoid exposing internal concrete types accidentally through public function signatures.
- Put feature-gated API behind additive, well-documented Cargo features.

## Cargo And Dependency Policy

- Use `cargo new` or `cargo init` so the initial manifest and layout match Cargo defaults.
- Commit `Cargo.toml` and `Cargo.lock` for applications. For libraries, commit `Cargo.lock` if the repository policy or CI benefits from reproducible checks.
- Keep dependencies small and actively maintained.
- Use workspace dependencies when a workspace has multiple crates sharing versions.
- Keep Cargo features additive. Do not make one feature disable behavior expected by another feature.
- Define a minimum supported Rust version when consumers need stability.
- Separate normal, dev, build, and target-specific dependencies.
- Avoid proc macros and large async stacks until the project needs them.
- Use `cargo update -p name` deliberately for targeted dependency updates.

Starter library manifest shape:

```toml
[package]
name = "project-name"
version = "0.1.0"
edition = "2024"
license = "MIT OR Apache-2.0"

[dependencies]

[dev-dependencies]
```

Use the edition that matches the project policy and toolchain. When publishing, fill in repository, description, readme, keywords/categories, and license metadata.

## Tooling Defaults

Recommended local commands:

```bash
cargo fmt --all
cargo fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
cargo nextest run --all-features
cargo test --doc
cargo build --all-targets --all-features
cargo tarpaulin --all-features
cargo machete
cargo deny check
cargo audit
cargo semver-checks check-release  # libraries only
cargo mutants                       # periodic, not every commit
cargo geiger                         # periodic, not every commit
```

Mandatory tools (run in every CI build):

- `cargo fmt` — formatting enforcement.
- `cargo clippy` — lint with `-D warnings` so all warnings fail the build.
- Cargo Nextest — primary test runner, faster and more reliable than `cargo test` for large suites.
- `cargo deny check` — dependency security vulnerabilities, restrictive licenses, banned/duplicate crates.
- `cargo audit` — checks `Cargo.lock` against the RustSec Advisory Database for known CVEs.
- `cargo tarpaulin` — code coverage measurement for Rust.
- `cargo machete` — finds unused dependencies in `Cargo.toml`.
- `cargo semver-checks` — ensures public API changes do not break Semantic Versioning (libraries).
- Miri — detects undefined behavior in `unsafe` code blocks; mandatory when the crate contains `unsafe`.
- rust-analyzer — IDE LSP for real-time diagnostics, type info, and refactor support.

Periodic tools (run regularly but not on every commit):

- `cargo mutants` — mutation testing to verify test suite effectiveness.
- `cargo geiger` — scans the full dependency graph for `unsafe` code usage.

## Testing And TDD

- Put unit tests in the module under `#[cfg(test)] mod tests`.
- Put public-contract integration tests in `tests/*.rs`.
- Put runnable usage examples in `examples/`.
- Use doc tests for public API examples that should compile and run.
- Start TDD with the smallest behavior: parser, value object, trait adapter, command runner, state transition, or error conversion.
- Test success, failure, boundary values, ownership-sensitive behavior, and serialization/deserialization if present.
- Prefer deterministic fixtures and temporary directories over global paths.
- For async code, use the runtime's test attribute consistently and keep timeouts explicit.
- For unsafe code, add tests for boundary conditions and run Miri in CI to detect undefined behavior.
- For parsers and protocol handling, add property tests with `proptest` or fuzzing when input space is broad.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Format | `cargo fmt --all -- --check` | Enforces rustfmt style. |
| Lint | `cargo clippy --all-targets --all-features -- -D warnings` | Catches common mistakes and maintainability issues. |
| Tests | `cargo nextest run --all-features` | Faster, more reliable test execution than `cargo test`. |
| Doc tests | `cargo test --doc` | Verifies public documentation examples. |
| Build | `cargo build --all-targets --all-features` | Compiles binaries, tests, examples, and feature paths. |
| Docs | `cargo doc --no-deps --all-features` | Ensures public docs build. |
| Coverage | `cargo tarpaulin --all-features` | Code coverage measurement. |
| Security (deps) | `cargo deny check` | Vulnerabilities, licenses, banned/duplicate crates. |
| Security (advisories) | `cargo audit` | Checks Cargo.lock against RustSec Advisory Database. |
| Unsafe audit | `cargo geiger` | Scans dependency graph for `unsafe` code usage. |
| Unused deps | `cargo machete` | Finds dependencies in Cargo.toml that are never imported. |
| SemVer | `cargo semver-checks check-release` | Detects accidental breaking API changes (libraries). |
| UB detection | `cargo miri test` | Detects undefined behavior in `unsafe` code. |
| Test quality | `cargo mutants` | Mutation testing to verify test effectiveness. |

For libraries with feature flags, also test default features, no-default-features, and important feature combinations. For embedded/no_std crates, include target-specific checks for supported targets.

## CI Baseline

```bash
rustc --version
cargo --version
cargo fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
cargo nextest run --all-features
cargo test --doc
cargo build --all-targets --all-features
cargo tarpaulin --all-features
cargo machete
cargo deny check
cargo audit
```

For library crates, add:

```bash
cargo semver-checks check-release
```

For crates with `unsafe` code, add:

```bash
cargo miri test
```

Run periodic tools (cargo-mutants, cargo-geiger) on a schedule (nightly/weekly) rather than every commit:

```bash
cargo mutants
cargo geiger
```

Cache Cargo registry, git, and target directories according to the CI platform. Avoid making CI depend on developer-local toolchain state; use `rust-toolchain.toml` when the project needs a pinned channel or minimum toolchain.

## Unsafe, FFI, And Security

- Add `#![forbid(unsafe_code)]` or `#![deny(unsafe_op_in_unsafe_fn)]` when it fits the project.
- If unsafe is required, isolate it in small modules and provide safe wrappers.
- Document safety invariants on every unsafe function, trait, and block that is not obvious.
- Validate FFI pointers, lengths, nullability, ownership, and threading assumptions at the boundary.
- Run Miri on all `unsafe` code to detect undefined behavior in CI.
- Run cargo-geiger periodically to audit the full dependency graph for `unsafe` code usage.
- Avoid leaking secrets through `Debug` implementations and logs.
- Be explicit about integer parsing, overflow expectations, path handling, and untrusted input limits.
- Run cargo-deny and cargo-audit in every CI build to track dependency advisories, license violations, and banned crates.

## Documentation

- Put crate-level docs in `src/lib.rs` with `//!` when publishing a library.
- Use rustdoc examples that show the normal path and meaningful error handling.
- Document feature flags, MSRV, safety guarantees, panic behavior, and error contracts.
- For CLIs, document config files, environment variables, exit codes, and example invocations.
- Keep README and rustdoc aligned; do not let one become stale marketing copy.

## Review Hot Spots

- Public APIs that expose internal types, lifetimes, or feature-gated details accidentally.
- `unwrap`, `expect`, `panic!`, and indexing in non-test paths.
- Overuse of `Arc<Mutex<_>>` instead of clearer ownership or message passing.
- Blocking calls inside async tasks.
- Cargo features that are not additive or are not tested together.
- Workspaces split before dependency, ownership, or release boundaries are real.
- Unsafe code without local safety comments and tests around edge cases.
- Error types that lose source errors or make caller recovery impossible.
- Tests that exercise implementation details but miss public API behavior.

## Planning Checklist

- Create crate with `cargo new` or `cargo init`.
- Add `src/lib.rs` for testable logic and keep `main.rs` thin.
- Add first failing test under `#[cfg(test)] mod tests`.
- Add rustfmt and Clippy (`-D warnings`) to CI.
- Add Cargo Nextest as the primary test runner.
- Add cargo-tarpaulin for coverage.
- Add cargo-deny and cargo-audit for dependency security.
- Add cargo-machete for unused dependency detection.
- Add cargo-semver-checks for library API stability.
- Configure Miri in CI if the crate contains `unsafe`.
- Add cargo-mutants and cargo-geiger to periodic CI schedules.
- Configure rust-analyzer for IDE integration.
