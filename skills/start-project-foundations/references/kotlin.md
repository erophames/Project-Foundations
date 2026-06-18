# Kotlin Best Practices

Sources:
- Kotlin coding conventions: https://kotlinlang.org/docs/coding-conventions.html
- Kotlin Gradle project configuration: https://kotlinlang.org/docs/gradle-configure-project.html
- Kotlin Gradle best practices: https://kotlinlang.org/docs/gradle-best-practices.html
- Kotlin JVM console tutorial: https://kotlinlang.org/docs/jvm-get-started.html
- Kotlin Multiplatform: https://kotlinlang.org/docs/multiplatform.html
- Kotlin coroutines: https://kotlinlang.org/docs/coroutines-overview.html
- KDoc: https://kotlinlang.org/docs/kotlin-doc.html
- ktlint: https://pinterest.github.io/ktlint/latest/
- detekt: https://detekt.dev/docs/intro/
- JUnit user guide: https://docs.junit.org/current/user-guide/
- Kotest: https://kotest.io/docs/framework/framework.html
- Android Kotlin style guide: https://developer.android.com/kotlin/style-guide

## Use This Reference

Apply this reference for Kotlin/JVM libraries, CLIs, backend services, Android projects, Kotlin Multiplatform projects, Gradle build logic written in Kotlin DSL, and mixed Java/Kotlin repositories where Kotlin owns part of the public boundary. Kotlin projects usually live in the JVM ecosystem, so reuse established JVM build and test defaults while leaning into Kotlin's null-safety, immutability, top-level declarations, coroutines, and concise domain modeling.

Default stance:

- Use Gradle with Kotlin DSL (`*.gradle.kts`) for new Kotlin projects.
- Use standard source sets: `src/main/kotlin` and `src/test/kotlin` for JVM projects.
- Use Kotlin's official coding conventions as the baseline.
- Use ktlint for formatting/style and detekt for static analysis/code smell checks.
- Use JUnit on the JVM by default; use Kotest when expressive property/data-driven styles are valuable.
- Keep Android and Multiplatform guidance layered on top of the base Kotlin rules.

## Default Structure

For a Kotlin/JVM library, CLI, or service:

```text
project-name/
|-- settings.gradle.kts
|-- build.gradle.kts
|-- gradle/
|   `-- libs.versions.toml
|-- src/
|   |-- main/
|   |   |-- kotlin/
|   |   |   `-- com/example/project/
|   |   `-- resources/
|   `-- test/
|       |-- kotlin/
|       |   `-- com/example/project/
|       `-- resources/
`-- README.md
```

For pure Kotlin projects, directory structure should follow the package structure with the common root package omitted when practical. For mixed Java/Kotlin JVM projects, place Kotlin files in the same package-aligned structure as Java files and keep source-set boundaries clear.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| JVM library | `src/main/kotlin`, `src/test/kotlin`, Gradle Kotlin DSL | Keep public API deliberate; add KDoc for exported types. |
| CLI | `src/main/kotlin/.../Main.kt`, application plugin, command runner tests | Keep `main()` thin and test command behavior without spawning every case. |
| Backend service | framework defaults plus domain/application packages | Ktor, Spring, Micronaut, and Quarkus can add conventions; keep domain code framework-light. |
| Android | Android Gradle plugin layout plus Kotlin source sets | Follow Android Kotlin style where it conflicts with general Kotlin style. |
| Multiplatform | `commonMain`, `commonTest`, platform source sets | Put shared logic in common code and isolate platform APIs behind `expect`/`actual`. |
| Build logic | `buildSrc` or included build convention plugins | Keep Gradle Kotlin DSL typed, small, and reusable. |

Avoid creating `Utils.kt`, `Helpers.kt`, or `Manager` classes by default. Use names that describe the responsibility: `MoneyFormatter.kt`, `InvoiceParser.kt`, `CustomerRepository.kt`.

## Naming And Style

- Use lowercase package names without underscores.
- Use `UpperCamelCase` for classes, interfaces, objects, enum classes, annotation classes, and type aliases.
- Use `lowerCamelCase` for functions, properties, local variables, and parameters.
- Use `UPPER_SNAKE_CASE` only for true constants: `const val` or deeply immutable top-level/object `val` values.
- Name files after their main class/interface when there is one. For related top-level declarations, use an `UpperCamelCase.kt` name that describes the content.
- In tests, backtick names with spaces are allowed on JVM; avoid them for Android tests that must run below API 30.
- Use four spaces, no tabs.
- Prefer expression bodies for simple functions.
- Group related class members together rather than sorting alphabetically.
- Omit redundant `public` modifiers outside libraries where explicit API mode is used.
- Prefer trailing commas at declaration sites when they reduce diff noise.

## API And Module Design

- Treat nullability as part of the contract. Avoid `!!` except at tiny boundaries where an invariant is immediately obvious.
- Prefer immutable `val` properties and read-only collection interfaces.
- Keep mutable state private and expose read-only views.
- Use `data class` for transparent value carriers, `value class` for domain wrappers, and `sealed` hierarchies for closed state/result models.
- Use top-level functions when they express package-level behavior clearly; do not create classes only to hold static-like functions.
- Use extension functions when they improve the call site and belong near the type or client that owns the behavior.
- Use `internal` for module-private APIs, especially in multi-module builds.
- Avoid broad service-locator singletons. `object` declarations are useful for stateless behavior or true process-wide singletons, not dependency management.
- Keep Java interop deliberate: use `@JvmName`, `@JvmOverloads`, and platform types only when required by callers.
- Add KDoc for public libraries and APIs whose usage is not obvious from type names.

## Coroutines And Concurrency

- Use `suspend` functions for asynchronous operations that return a single result.
- Use structured concurrency: launch coroutines from a lifecycle-owned `CoroutineScope`.
- Avoid `GlobalScope` in application code.
- Inject dispatchers or coroutine contexts at boundaries where tests need control.
- Use `Flow` for cold streams, `StateFlow` for observable state, and `SharedFlow` for broadcast-style events.
- Keep blocking IO off default/main dispatchers.
- Always test cancellation, failure, and timeout behavior for coroutine-heavy code.
- Prefer `runTest` from kotlinx-coroutines-test for coroutine tests when the project uses coroutines.

## Build And Dependency Policy

- Use Gradle Kotlin DSL for new builds.
- Use a version catalog (`gradle/libs.versions.toml`) when dependency count is non-trivial or the project has multiple modules.
- Use convention plugins once repeated Gradle configuration appears in more than one module.
- Pin the JVM toolchain instead of relying on the developer's ambient JDK.
- Keep framework dependencies in boundary modules; core/domain modules should usually depend only on Kotlin/JVM basics.
- Avoid mixing Maven and Gradle builds unless migration is in progress.
- For published libraries, configure explicit API, metadata, license, repository, and binary compatibility checks if public API stability matters.

Starter JVM `build.gradle.kts` shape:

```kotlin
plugins {
    kotlin("jvm")
    application
}

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(21)
}

dependencies {
    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}
```

For real projects, pin plugin and dependency versions through `settings.gradle.kts` plugin management or `gradle/libs.versions.toml`.

## Tooling Defaults

- Formatter/style: ktlint, ideally wired through Gradle.
- Static analysis: detekt with `buildUponDefaultConfig`.
- Tests: JUnit for conservative JVM compatibility; Kotest for richer style/data/property testing.
- Coverage: Kover or JaCoCo when coverage reporting is needed.
- Docs: KDoc plus Dokka for published libraries.
- Android: Android Studio formatter and Android Kotlin style where Android-specific rules apply.

Recommended commands:

```bash
./gradlew test
./gradlew ktlintCheck
./gradlew detekt
./gradlew build
```

Task names depend on the chosen ktlint/detekt Gradle plugins. Use the project wrapper and check available tasks with `./gradlew tasks`.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Tests | `./gradlew test` | JVM behavior and regression coverage. |
| Format/style | `./gradlew ktlintCheck` | Kotlin coding convention enforcement. |
| Static analysis | `./gradlew detekt` | Complexity, code smells, and maintainability checks. |
| Build | `./gradlew build` | Compile, test, package, and configured checks. |
| Docs | `./gradlew dokkaHtml` | Public library documentation when enabled. |
| Multiplatform | `./gradlew allTests` or target-specific test tasks | Ensures common and platform code compile/test. |

For Android projects, include Android-specific unit/instrumented test tasks and lint. For server projects, add startup/config smoke tests and integration tests for database/HTTP boundaries.

## TDD Guidance

- Put JVM tests under `src/test/kotlin` with names ending in `Test`.
- Start with one behavior at the public boundary: parser, service, repository adapter, CLI runner, coroutine use case, or domain function.
- Use Kotlin's test assertions, JUnit Jupiter, or Kotest consistently.
- Use backtick test names for readable JVM tests when they improve intent.
- Test nullable inputs, sealed-state branches, coroutine cancellation, and exception/result paths.
- Prefer real value objects and fake adapters over heavy mocking.
- For Android, test pure ViewModel/use-case/domain code as local unit tests before adding instrumented tests.
- For Multiplatform, put shared behavior tests in `commonTest` and platform-specific tests in target source sets.

## Android And Multiplatform Notes

- Android projects should follow Android architecture and lifecycle constraints. Keep UI, ViewModel, domain, and data responsibilities separate.
- Avoid leaking Android framework types into shared/domain modules.
- In Multiplatform projects, keep `commonMain` free of platform APIs unless wrapped by `expect`/`actual`.
- Name platform-specific files with source-set suffixes when they contain top-level declarations, for example `Platform.jvm.kt` or `Platform.android.kt`, to avoid duplicate JVM facade class problems.
- Keep shared code small at first; do not force platform-specific UI or storage into common code unless the abstraction is stable.

## CI Baseline

```bash
./gradlew --version
./gradlew ktlintCheck
./gradlew detekt
./gradlew test
./gradlew build
```

Use the Gradle wrapper in CI. Cache Gradle dependencies/build cache according to the CI platform. For Android, add lint and instrumented tests only when the CI environment supports the required SDK/emulator setup.

## Review Hot Spots

- `!!` and unsafe casts hiding weak boundaries.
- Platform types from Java APIs treated as non-null without validation.
- Coroutine scopes that outlive their owner.
- `GlobalScope`, blocking calls on main/default dispatchers, and missing cancellation paths.
- Overuse of `object` singletons for stateful dependencies.
- Domain logic inside framework controllers, Android activities/fragments, or Gradle build scripts.
- Multiplatform abstractions that mirror platform APIs instead of modeling project needs.
- Tests that only verify mocks rather than Kotlin behavior and state transitions.
