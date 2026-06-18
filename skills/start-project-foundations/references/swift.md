# Swift Best Practices

Sources:
- Swift API Design Guidelines: https://www.swift.org/documentation/api-design-guidelines/
- Swift Package Manager: https://www.swift.org/package-manager/
- Swift book: https://docs.swift.org/swift-book/documentation/the-swift-programming-language/guidedtour/
- swift-format: https://github.com/swiftlang/swift-format
- SwiftLint: https://github.com/realm/SwiftLint

## Use This Reference

Apply this reference when Swift owns an iOS, macOS, watchOS, tvOS, server-side Swift, command-line, or Swift package project. Swift projects should lean on Swift Package Manager where possible, follow Swift API design guidelines, make value semantics explicit, and keep Apple-platform lifecycle/UI code separated from domain behavior.

Default stance:

- Use Swift Package Manager for libraries, CLIs, and server packages.
- Use Xcode project/workspace conventions for Apple apps.
- Use XCTest or Swift Testing according to project/toolchain support.
- Use swift-format or SwiftLint/SwiftFormat consistently; do not mix competing style authorities casually.
- Keep UI, state, domain, and IO boundaries testable.

## Default Structure

For a Swift package:

```text
project-name/
|-- Package.swift
|-- Sources/
|   `-- ProjectName/
|       `-- ProjectName.swift
|-- Tests/
|   `-- ProjectNameTests/
|       `-- ProjectNameTests.swift
`-- README.md
```

For a CLI package:

```text
project-name/
|-- Package.swift
|-- Sources/
|   |-- ProjectCore/
|   `-- project-cli/
|       `-- main.swift
`-- Tests/
    `-- ProjectCoreTests/
```

For Apple apps, keep generated app structure but move reusable logic into packages, frameworks, or clearly separated modules when it grows beyond UI coordination.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Swift package | `Package.swift`, `Sources/`, `Tests/` | Best for libraries and shared domain code. |
| CLI | Thin executable target plus library target | Test the library target, not process exit for every case. |
| iOS/macOS app | Xcode app target plus app/domain modules | Keep view lifecycle code thin. |
| SwiftUI app | Views, models/state, services separated | Keep side effects out of view bodies. |
| Server Swift | Package layout plus framework routes/adapters | Keep route handlers thin and async boundaries explicit. |

## Naming And Style

- Follow Swift API Design Guidelines.
- Use `UpperCamelCase` for types and protocols.
- Use `lowerCamelCase` for functions, methods, variables, constants, enum cases, and labels.
- Name booleans and predicates so use sites read naturally: `isEnabled`, `hasAccess`.
- Prefer clear names over abbreviations.
- Omit needless words when the type context already communicates them.
- Use argument labels to make call sites read as phrases.
- Prefer nouns for types and protocols that model entities; use capability suffixes such as `-able` only when natural.
- Keep access control explicit: start `internal`/private, expose `public` deliberately.

## API And Module Design

- Prefer value types (`struct`, `enum`) for simple data and state.
- Use classes when identity, reference sharing, inheritance, or Objective-C interoperability is required.
- Use `let` by default; use `var` only for mutation.
- Model closed states with enums and associated values.
- Use optionals for absence; avoid force unwraps outside tests or immediately proven invariants.
- Use throwing functions for recoverable failures and typed result/state values where callers need explicit branching.
- Keep async APIs structured with `async`/`await`; avoid detached tasks unless lifetime is deliberate.
- Inject clocks, clients, file systems, and schedulers where tests need control.
- Keep Objective-C bridging and UIKit/AppKit types at platform boundaries.

## Tooling Defaults

Recommended Swift package commands:

```bash
swift package resolve
swift test
swift build
swift package diagnose-api-breaking-changes
```

Formatting/linting depends on the selected tool:

```bash
swift-format format --recursive --in-place Sources Tests
swift-format lint --recursive Sources Tests
swiftlint
```

For Xcode projects:

```bash
xcodebuild test -scheme SchemeName -destination 'platform=iOS Simulator,name=iPhone 16'
```

Use the concrete destination and scheme for the project; do not leave CI relying on the developer's selected simulator.

## Testing And TDD

- Put package tests under `Tests/<TargetName>Tests/`.
- Start with one failing test for a public function, reducer/state transition, parser, service, or view model.
- Use XCTest unless the project has adopted Swift Testing.
- Test pure domain/model code before UI automation.
- Use fakes for network, persistence, time, and notification dependencies.
- Test optional handling, thrown errors, cancellation, and main-actor behavior.
- For SwiftUI, test state/view models and use UI tests only for end-to-end flows.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Build | `swift build` | Compiles package targets. |
| Tests | `swift test` | Runs package tests. |
| Format/lint | `swift-format lint ...` or `swiftlint` | Enforces style. |
| Xcode tests | `xcodebuild test ...` | Runs app/framework tests. |
| Package resolve | `swift package resolve` | Verifies dependency graph. |

For Apple apps, include unit tests and at least one app launch/smoke test in CI when simulator availability is reliable.

## CI Baseline

For Swift packages:

```bash
swift --version
swift package resolve
swift build
swift test
swift-format lint --recursive Sources Tests
```

For Xcode apps, use `xcodebuild -list` to verify schemes and run explicit scheme/destination commands. Cache SwiftPM and DerivedData carefully; stale caches can hide package resolution issues.

## Security And Robustness

- Avoid force unwraps and force casts in production paths.
- Keep Keychain, file protection, permissions, and privacy prompts in explicit platform adapters.
- Validate server/API responses before mapping to domain types.
- Treat concurrency isolation warnings as design feedback.
- Keep secrets out of plists, sample configs, and logs.
- Avoid storing sensitive state in UserDefaults.

## Review Hot Spots

- Massive view controllers/views with business logic.
- `!`, `as!`, `try!`, and detached tasks.
- Main-thread assumptions in async code.
- Public API names that do not read clearly at call sites.
- Shared mutable reference state where value semantics would be simpler.
- Tests that only launch UI and miss domain behavior.
- Xcode schemes or package products not covered by CI.
