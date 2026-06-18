# Go Best Practices

Sources:
- Effective Go: https://go.dev/doc/effective_go
- Organizing a Go module: https://go.dev/doc/modules/layout
- Create a Go module: https://go.dev/doc/tutorial/create-module
- Go Doc Comments: https://go.dev/doc/comment
- `testing` package: https://pkg.go.dev/testing
- `go vet`: https://pkg.go.dev/cmd/vet
- Go fuzzing: https://go.dev/doc/security/fuzz/
- Govulncheck: https://go.dev/blog/govulncheck

## Use This Reference

Apply this reference when Go owns the main deliverable: a package, CLI, HTTP/gRPC service, background worker, infrastructure tool, or multi-command repository. Start with Go's standard toolchain before adding framework or layout conventions. Go projects should be small, package-oriented, formatted automatically, and verified with the built-in test, vet, race, and module tools.

Default stance:

- Use Go modules for every new project.
- Keep the root small: `go.mod`, `go.sum`, README, source packages, and tests.
- Start with simple package directories. Add `cmd/`, `internal/`, or workspaces only when the project shape needs them.
- Use `gofmt` or `go fmt` as the non-negotiable formatter.
- Use table-driven tests and subtests for behavior variants.
- Prefer the standard library until a dependency clearly pays for itself.

## Default Structure

For a single package library:

```text
project-name/
|-- go.mod
|-- go.sum
|-- README.md
|-- package.go
|-- package_test.go
`-- testdata/
```

For a CLI or service with one binary:

```text
project-name/
|-- go.mod
|-- go.sum
|-- README.md
|-- cmd/
|   `-- project-name/
|       `-- main.go
|-- internal/
|   |-- app/
|   |   `-- app.go
|   `-- config/
|       `-- config.go
`-- testdata/
```

For multiple commands, add more subdirectories under `cmd/`. For shared code that should not be imported by external modules, use `internal/`. Avoid adding `pkg/` by default; reserve it for packages that are intentionally public and reusable outside the module.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Library module | Root package or focused package directories | Keep exported API small and document exported identifiers. |
| CLI | `cmd/name/main.go`, internal command runner package | Keep `main` thin; test parsing and execution through ordinary functions. |
| HTTP/gRPC service | `cmd/service`, `internal/app`, `internal/config`, boundary packages | Keep handlers/adapters thin and domain behavior testable without a server. |
| Multiple binaries | One `cmd/<name>/main.go` per executable | Share private code through `internal/`, not copied command logic. |
| Multi-module repo | `go.work` plus independent module roots | Use only when modules must version/build independently. |
| Generated/API project | `api/` or generator-owned folders plus checked-in config | Keep generated code boundaries clear and do not edit generated files manually. |

Avoid creating large `utils`, `common`, or `helpers` packages. Package names should describe the domain they provide: `invoice`, `retry`, `postgres`, `httpclient`, `authz`.

## Naming And Style

- Let `gofmt` decide formatting. Do not hand-align code against it.
- Use tabs for indentation as produced by `gofmt`.
- Use short, lowercase, single-word package names when possible. Avoid underscores and mixed case in package names.
- Use `MixedCaps` or `mixedCaps` for multiword identifiers, not underscores.
- Exported identifiers begin with an uppercase letter and need doc comments in public packages.
- Avoid package-name stutter: prefer `cache.Store` over `cache.CacheStore` when the package context is already clear.
- Keep receiver names short and consistent across methods on the same type.
- Name one-method interfaces after the method with an `-er` style when natural, such as `Reader`, `Writer`, `Encoder`.
- Prefer `ErrNotFound` for sentinel errors and `NotFoundError` style names for error types when callers need structured matching.
- Do not use `Get` prefixes for ordinary getters. A method named `Owner()` is idiomatic; `GetOwner()` usually is not.
- Keep comments as sentences for exported API. Use package comments for non-trivial packages and commands.

## API And Package Design

- Design packages around behavior and ownership, not architectural layers copied from other languages.
- Keep package APIs small. Export only what callers need.
- Accept interfaces at the consumer side when they make tests or substitution simpler; return concrete types unless callers need an abstraction.
- Put `context.Context` as the first parameter after any receiver for operations that can block, perform IO, or cross process boundaries.
- Return `error` as the last return value.
- Prefer explicit error handling. Do not panic for normal validation, IO, network, or dependency failures.
- Wrap errors with context when crossing boundaries, and preserve matchability with `%w` when callers need `errors.Is` or `errors.As`.
- Make zero values useful where practical. Avoid requiring constructors only to make an object non-crashing.
- Keep concurrency visible. Use goroutines, channels, mutexes, and contexts deliberately, not hidden behind surprising package globals.
- Avoid package-level mutable state except for constants, stateless helpers, and carefully documented singletons.
- Keep `init` functions rare. Prefer explicit setup from `main` or tests.

## Modules And Dependencies

- Initialize with `go mod init <module-path>`.
- Keep module paths stable; changing them is a breaking import-path change for libraries.
- Run `go mod tidy` after adding or removing imports.
- Commit `go.mod` and `go.sum`.
- Avoid vendoring unless the environment requires it. If vendoring is used, make it a deliberate build policy.
- Prefer stable, narrow dependencies. Avoid framework-wide packages for small needs that the standard library covers.
- Use `go work` for local multi-module development only when a repository truly contains multiple modules.
- Keep generated clients, protobuf output, or OpenAPI output behind clear commands and review generated changes separately.

## Tooling Defaults

Recommended local commands:

```bash
go fmt ./...
go vet ./...
go test ./...
go test -race ./...
govulncheck ./...
go build ./...
```

Optional tools:

- `goimports` for import formatting and grouping when available.
- `staticcheck` for deeper static analysis on mature projects.
- `golangci-lint` when the team wants a single lint runner, configured conservatively.
- `goreleaser` for multi-platform CLI releases.

Do not start with a large lint preset. Add checks when they catch real issues without fighting Go's normal style.

## Testing And TDD

- Put tests beside the package in files ending with `_test.go`.
- Name tests `TestXxx`, benchmarks `BenchmarkXxx`, examples `ExampleXxx`, and fuzz tests `FuzzXxx`.
- Start TDD at the smallest public behavior: parser, validator, service method, command runner, repository adapter, or handler.
- Use table-driven tests for input/output variants.
- Use `t.Run` subtests when cases need names or independent setup.
- Use `t.Helper()` in helper assertions to improve failure locations.
- Use `testdata/` for fixtures that tests read from disk.
- Test exported API from an external test package (`package name_test`) when you want to verify the public contract only.
- Use same-package tests (`package name`) when internals need direct testing during package development.
- Use `httptest`, `fstest`, `iotest`, fake clocks, and small fake interfaces before heavy mocking frameworks.
- Run `go test -race ./...` for concurrent code and services.
- Add fuzz tests for parsers, decoders, protocol handling, and untrusted input boundaries. Keep fuzz targets deterministic and fast.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Format | `go fmt ./...` | Applies canonical formatting. |
| Static checks | `go vet ./...` | Finds suspicious constructs with the official analyzer. |
| Tests | `go test ./...` | Runs unit, integration, examples, and seed fuzz cases. |
| Race | `go test -race ./...` | Detects data races in test-covered concurrent paths. |
| Build | `go build ./...` | Confirms all packages and commands compile. |
| Vulnerabilities | `govulncheck ./...` | Reports reachable known vulnerabilities. |
| Fuzz | `go test -fuzz=FuzzName ./path` | Exercises selected untrusted-input code paths. |

For services, add an integration test target for database, queue, HTTP, or RPC boundaries. Keep slow tests behind a clear build tag or environment gate.

## CI Baseline

```bash
go version
go mod tidy
go fmt ./...
go vet ./...
go test ./...
go test -race ./...
go build ./...
govulncheck ./...
```

In CI, fail if `go mod tidy` changes files. Cache the Go build and module caches according to the CI platform. Keep race tests if runtime is acceptable; otherwise run them on main branch or nightly at minimum for concurrent services.

## Documentation

- Add package comments for public packages whose purpose is not obvious.
- Add doc comments for exported identifiers.
- Prefer runnable examples for public packages when examples clarify API usage.
- Document environment variables, config files, and command behavior in README or command package docs.
- For CLIs, make `-h` output useful and test command parsing separately from process exit behavior.

## Review Hot Spots

- Large packages named `common`, `utils`, or `helpers`.
- Logic hidden in `main`, `init`, package globals, or HTTP handlers.
- Goroutines without cancellation, ownership, or error reporting.
- Context ignored at network, database, or process boundaries.
- Errors discarded with `_` or replaced with generic messages that lose root cause.
- Public package stutter and exported API without comments.
- Tests that only cover happy paths or depend on real network/time/global state.
- Dependencies added for small standard-library capabilities.
- Race-prone maps, caches, or shared mutable structs without synchronization.
