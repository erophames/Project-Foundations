# Kotlin Best Practices

Sources:
- Kotlin coding conventions: https://kotlinlang.org/docs/coding-conventions.html
- Maven Kotlin plugin: https://kotlinlang.org/docs/maven.html
- Kotlin JVM getting started: https://kotlinlang.org/docs/jvm-get-started.html
- Kotlin Multiplatform: https://kotlinlang.org/docs/multiplatform.html
- Kotlin coroutines: https://kotlinlang.org/docs/coroutines-overview.html
- KDoc: https://kotlinlang.org/docs/kotlin-doc.html
- Ktfmt: https://github.com/facebook/ktfmt
- detekt: https://detekt.dev/docs/intro/
- Konsist: https://docs.konsist.lemonappdev.com/
- JUnit user guide: https://docs.junit.org/current/user-guide/
- Kotest: https://kotest.io/docs/framework/framework.html
- Android Kotlin style guide: https://developer.android.com/kotlin/style-guide
- MVIKotlin: https://github.com/arkivanov/MVIKotlin
- Orbit MVI: https://github.com/orbit-mvi/orbit-mvi
- Maven Versions Plugin: https://www.mojohaus.org/versions/versions-maven-plugin/

## Use This Reference

Apply this reference for Kotlin/JVM libraries, CLIs, backend services, Android projects, Kotlin Multiplatform projects, Gradle build logic written in Kotlin DSL, and mixed Java/Kotlin repositories where Kotlin owns part of the public boundary. Kotlin projects usually live in the JVM ecosystem, so reuse established JVM build and test defaults while leaning into Kotlin's null-safety, immutability, top-level declarations, coroutines, and concise domain modeling.

Default stance:

- Use Maven with the Kotlin Maven plugin for new Kotlin/JVM projects.
- Manage all dependency and plugin versions through POM `<properties>`.
- Use standard Maven source layout: `src/main/kotlin` and `src/test/kotlin` for JVM projects.
- Enable Kotlin strict mode (`allWarningsAsErrors`) so the compiler rejects suspicious code.
- Use Ktfmt (Meta's Kotlin formatter) for deterministic formatting enforcement.
- Use detekt with `buildUponDefaultConfig` for static analysis and code smell checks.
- Use Konsist for architecture enforcement through executable tests.
- Use JUnit on the JVM by default; use Kotest when expressive property/data-driven styles are valuable.
- Keep Android and Multiplatform guidance layered on top of the base Kotlin rules.
- Use MVIKotlin or Orbit MVI for state management in Android projects.

## Default Structure

For a Kotlin/JVM library, CLI, or service with Maven:

```text
project-name/
|-- pom.xml
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
| JVM library | `src/main/kotlin`, `src/test/kotlin`, Maven + kotlin-maven-plugin | Keep public API deliberate; add KDoc for exported types. |
| CLI | `src/main/kotlin/.../Main.kt`, application, command runner tests | Keep `main()` thin and test command behavior without spawning every case. |
| Backend service | framework defaults plus domain/application packages | Ktor, Spring, Micronaut, and Quarkus can add conventions; keep domain code framework-light. |
| Android | Android Gradle plugin layout plus Kotlin source sets | Follow Android Kotlin style where it conflicts with general Kotlin style. |
| Multiplatform | `commonMain`, `commonTest`, platform source sets | Put shared logic in common code and isolate platform APIs behind `expect`/`actual`. |

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

- Use Maven with the Kotlin Maven plugin for new builds.
- Manage all dependency and plugin versions through POM `<properties>` so upgrades stay in one place.
- Enable Kotlin strict mode: configure `allWarningsAsErrors` in the kotlin-maven-plugin so the compiler treats warnings as errors.
- Pin the JVM target version through the kotlin-maven-plugin `<jvmTarget>` configuration.
- Keep framework dependencies in boundary modules; core/domain modules should usually depend only on Kotlin/JVM basics.
- Use the versions-maven-plugin to detect outdated dependencies regularly.
- For published libraries, configure explicit API metadata, license, repository, and binary compatibility checks if public API stability matters.

Starter Maven `pom.xml` shape:

```xml
<properties>
    <kotlin.version>2.0.20</kotlin.version>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>21</maven.compiler.release>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.jetbrains.kotlin</groupId>
            <artifactId>kotlin-maven-plugin</artifactId>
            <version>${kotlin.version}</version>
            <configuration>
                <jvmTarget>21</jvmTarget>
                <allWarningsAsErrors>true</allWarningsAsErrors>
            </configuration>
        </plugin>
        <plugin>
            <groupId>com.facebook</groupId>
            <artifactId>ktfmt-maven-plugin</artifactId>
        </plugin>
        <plugin>
            <groupId>com.github.gantsign.maven</groupId>
            <artifactId>detekt-maven-plugin</artifactId>
        </plugin>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>versions-maven-plugin</artifactId>
        </plugin>
    </plugins>
</build>
```

For real projects, pin all plugin versions through `<properties>`.

## Tooling Defaults

- Formatter: Ktfmt (Meta's Kotlin formatter) wired through Maven for deterministic formatting.
- Static analysis: detekt with `buildUponDefaultConfig` for complexity, code smells, and maintainability checks.
- Architecture testing: Konsist for enforcing layering, package dependency rules, and naming conventions through executable tests.
- Compiler strict mode: `allWarningsAsErrors` in the kotlin-maven-plugin so suspicious code fails the build.
- Tests: JUnit for conservative JVM compatibility; Kotest for richer style/data/property testing.
- Coverage: JaCoCo when coverage reporting is needed.
- Docs: KDoc plus Dokka for published libraries.
- Dependency freshness: versions-maven-plugin for update detection.
- Android: Android Studio formatter and Android Kotlin style where Android-specific rules apply.

Recommended Maven commands:

```bash
./mvnw test
./mvnw ktfmt:check
./mvnw detekt:check
./mvnw verify
./mvnw versions:display-dependency-updates
```

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Compiler strict mode | kotlin-maven-plugin `allWarningsAsErrors` | Rejects suspicious code at compile time. |
| Tests | `./mvnw test` | JVM behavior and regression coverage. |
| Format | `./mvnw ktfmt:check` | Deterministic Ktfmt formatting enforcement. |
| Static analysis | `./mvnw detekt:check` | Complexity, code smells, and maintainability checks. |
| Architecture | Konsist test suite (`./mvnw test`) | Layer, package dependency, and naming rule enforcement. |
| Full verification | `./mvnw verify` | Compile, test, package, and configured checks. |
| Docs | `./mvnw dokka:dokka` | Public library documentation when enabled. |
| Dependency freshness | `./mvnw versions:display-dependency-updates` | Detect outdated dependencies. |
| Multiplatform | target-specific test tasks | Ensures common and platform code compile/test. |

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
- Use MVIKotlin or Orbit MVI for unidirectional state management. Both provide testable state containers that keep business logic out of ViewModels and Fragments.
  - MVIKotlin suits projects needing full MVI with intent-driven state reduction and Android lifecycle-aware stores.
  - Orbit MVI suits projects wanting a lightweight MVI container with simpler API and ViewModel integration.
- Avoid leaking Android framework types into shared/domain modules.
- In Multiplatform projects, keep `commonMain` free of platform APIs unless wrapped by `expect`/`actual`.
- Name platform-specific files with source-set suffixes when they contain top-level declarations, for example `Platform.jvm.kt` or `Platform.android.kt`, to avoid duplicate JVM facade class problems.
- Keep shared code small at first; do not force platform-specific UI or storage into common code unless the abstraction is stable.

## CI Baseline

```bash
./mvnw --version
./mvnw ktfmt:check
./mvnw detekt:check
./mvnw test
./mvnw verify
./mvnw versions:display-dependency-updates
```

Cache Maven dependencies according to the CI platform. For Android, add lint and instrumented tests only when the CI environment supports the required SDK/emulator setup.

## Architecture Testing

Use Konsist to enforce architectural rules as executable Kotlin tests that fail the build when violated:

- **Layer dependencies:** domain packages must not import infrastructure or UI framework types.
- **Package structure:** classes in domain packages must not reside outside expected modules.
- **Naming conventions:** ViewModels must end in `ViewModel`, repositories in `Repository`.
- **Framework isolation:** shared/common code must not import Android-specific types.

Konsist tests live alongside regular unit tests in `src/test/kotlin` and run as part of `./mvnw test`. Treat architecture violations as build failures, not warnings.

## Review Hot Spots

- `!!` and unsafe casts hiding weak boundaries.
- Platform types from Java APIs treated as non-null without validation.
- Kotlin strict mode warnings suppressed or downgraded without justification.
- Coroutine scopes that outlive their owner.
- `GlobalScope`, blocking calls on main/default dispatchers, and missing cancellation paths.
- Overuse of `object` singletons for stateful dependencies.
- Domain logic inside framework controllers, Android activities/fragments, or Maven build configuration.
- Multiplatform abstractions that mirror platform APIs instead of modeling project needs.
- Tests that only verify mocks rather than Kotlin behavior and state transitions.

## Planning Checklist

- Create `pom.xml` with the Kotlin Maven plugin and `<properties>` for all versions.
- Enable Kotlin strict mode (`allWarningsAsErrors`).
- Add `src/main/kotlin` and `src/test/kotlin`.
- Add first failing JUnit 5 test.
- Add Ktfmt and detekt checks to local verification.
- Add Konsist tests for layer and package dependency rules.
- Add versions-maven-plugin to CI.
- For Android, choose MVIKotlin or Orbit MVI for state management.
