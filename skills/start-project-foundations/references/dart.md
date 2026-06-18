# Dart Best Practices

Sources:
- Effective Dart: https://dart.dev/effective-dart
- Dart package layout: https://dart.dev/tools/pub/package-layout
- dart analyze: https://dart.dev/tools/dart-analyze
- dart format: https://dart.dev/tools/dart-format
- Dart `test` package: https://pub.dev/packages/test
- Flutter testing overview: https://docs.flutter.dev/testing/overview

## Use This Reference

Apply this reference when Dart owns a package, CLI, server tool, Flutter app, Flutter package, or shared Dart library. Dart projects should follow Effective Dart, use Pub package layout, keep analysis clean, and separate Flutter UI from testable state/domain logic.

Default stance:

- Use `pubspec.yaml` and standard Pub layout.
- Use `dart format` and `dart analyze`.
- Use `package:test` for Dart packages and Flutter test tools for Flutter apps.
- Keep generated files and source files clearly separated.
- Prefer null-safe, typed APIs and explicit async behavior.

## Default Structure

For a Dart package:

```text
project-name/
|-- pubspec.yaml
|-- analysis_options.yaml
|-- lib/
|   |-- project_name.dart
|   `-- src/
|       `-- feature.dart
|-- test/
|   `-- feature_test.dart
`-- README.md
```

For a CLI:

```text
project-name/
|-- pubspec.yaml
|-- bin/
|   `-- project_name.dart
|-- lib/
|   `-- src/
|       `-- command_runner.dart
`-- test/
```

For Flutter, follow Flutter's generated app/package layout and keep reusable logic under `lib/` in testable classes/functions.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Dart package | `lib/project_name.dart`, `lib/src/`, `test/` | Export only intended API from the top-level library. |
| CLI | `bin/`, `lib/src/`, `test/` | Keep `main()` thin and command behavior testable. |
| Flutter app | `lib/`, `test/`, `integration_test/` | Separate widgets, state, services, and domain logic. |
| Flutter package | Package layout plus example app | Include an `example/` when useful for consumers. |
| Generated-code project | `build_runner` outputs clearly marked | Do not edit generated `.g.dart` files manually. |

## Naming And Style

- Follow Effective Dart.
- Use `lowerCamelCase` for variables, parameters, members, and functions.
- Use `UpperCamelCase` for classes, enums, typedefs, extensions, and type parameters.
- Use `lowercase_with_underscores` for packages, directories, and source files.
- Use leading underscores for library-private declarations.
- Prefer `final` for variables that are not reassigned.
- Avoid abbreviations unless they are more readable than the full name.
- Keep public API documented for packages.

## API And Module Design

- Export only public API from `lib/project_name.dart`; keep implementation under `lib/src/`.
- Use null safety as part of the contract. Avoid `!` unless an invariant is immediate and obvious.
- Prefer immutable models where practical.
- Use sealed classes/enums/patterns for closed state when supported by the target SDK.
- Keep async APIs explicit with `Future` and `Stream`.
- Validate JSON and external data before constructing domain objects.
- Keep Flutter `BuildContext` and widget lifecycle concerns out of domain services.
- Inject clients, clocks, storage, and platform services for tests.

## Pub And Dependency Policy

- Define SDK constraints in `pubspec.yaml`.
- Commit `pubspec.lock` for applications. Package lock-file policy depends on repo convention.
- Keep dependencies small and use `dev_dependencies` for test/build/analyzer tools.
- Use `dependency_overrides` only temporarily and never as hidden long-term policy.
- Keep generated code commands documented when using `build_runner`.

## Tooling Defaults

Recommended Dart commands:

```bash
dart pub get
dart format --set-exit-if-changed .
dart analyze
dart test
dart compile exe bin/project_name.dart
```

Flutter commands:

```bash
flutter pub get
dart format --set-exit-if-changed .
flutter analyze
flutter test
flutter build apk
```

Use platform-specific Flutter build commands only for supported targets.

## Testing And TDD

- Put Dart tests under `test/` and name files `*_test.dart`.
- Start with one failing test for a function, parser, repository adapter, command runner, state object, or widget behavior.
- Use `package:test` for pure Dart.
- Use `flutter_test` for widgets and `integration_test` for end-to-end Flutter flows.
- Test async streams, errors, null/empty inputs, and platform-service failures.
- Prefer fake services over real network/storage in unit tests.
- Keep golden tests stable and intentional; do not use broad screenshots as a substitute for behavior tests.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Dependencies | `dart pub get` | Resolves packages. |
| Format | `dart format --set-exit-if-changed .` | Enforces formatting. |
| Static analysis | `dart analyze` | Runs analyzer and lint rules. |
| Tests | `dart test` or `flutter test` | Runs behavior tests. |
| Build | `dart compile ...` or `flutter build ...` | Confirms target builds. |

## CI Baseline

For Dart packages:

```bash
dart --version
dart pub get
dart format --set-exit-if-changed .
dart analyze
dart test
```

For Flutter:

```bash
flutter --version
flutter pub get
dart format --set-exit-if-changed .
flutter analyze
flutter test
```

Add build commands for the platforms the project claims to support.

## Security And Robustness

- Validate decoded JSON and platform-channel inputs.
- Avoid logging tokens, auth headers, and personally identifiable data.
- Keep platform permissions and entitlements minimal.
- Handle offline, timeout, cancellation, and app lifecycle transitions in Flutter apps.
- Avoid storing sensitive data in plain shared preferences.

## Review Hot Spots

- Public API leaking `lib/src` implementation details.
- Force unwraps and `dynamic` hiding boundary validation.
- Widget trees containing business logic.
- Untested async streams and cancellation.
- Generated files edited by hand.
- Analyzer warnings ignored instead of addressed.
