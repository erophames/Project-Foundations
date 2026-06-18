# Java Best Practices

Sources:
- Google Java Style Guide: https://google.github.io/styleguide/javaguide.html
- Maven standard directory layout: https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html
- Gradle Java plugin: https://docs.gradle.org/current/userguide/java_plugin.html
- JUnit 5 user guide: https://junit.org/junit5/docs/current/user-guide/
- Error Prone: https://errorprone.info/
- Spotless: https://github.com/diffplug/spotless
- JaCoCo: https://www.jacoco.org/jacoco/trunk/doc/
- SpotBugs: https://spotbugs.github.io/

## Use This Reference

Apply this reference for Java libraries, CLIs, services, JVM applications, Android-adjacent pure Java modules, and framework projects where Java is the primary language. Framework-specific conventions can add structure, but they should not erase the standard Maven/Gradle source layout or the separation between domain logic and framework glue.

Default stance:

- Use standard Maven/Gradle source layout.
- Pick Maven for conventional/simple builds and Gradle for builds that need richer customization.
- Add wrapper scripts for reproducible local and CI execution.
- Use JUnit 5 for tests.
- Enforce formatting in the build, not only in IDE settings.

## Default Structure

Use the standard Maven/Gradle source layout:

```text
project-name/
|-- pom.xml or build.gradle
|-- src/
|   |-- main/
|   |   |-- java/
|   |   |   `-- com/example/project/
|   |   `-- resources/
|   `-- test/
|       |-- java/
|       |   `-- com/example/project/
|       `-- resources/
`-- README.md
```

Use Maven for simple libraries and services when the user has no build preference. Use Gradle when the project needs more build customization or already uses Gradle.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Library | `src/main/java`, `src/test/java`, publish metadata | Keep public packages intentional and documented. |
| CLI | `src/main/java/.../Main.java`, service classes, tests | Keep `main()` thin; test command runner separately. |
| Service | framework defaults plus domain/application packages | Keep controllers/adapters thin and domain services testable. |
| Multi-module | root build plus one module per deployable/library boundary | Add modules only for real ownership or dependency boundaries. |
| Legacy app | preserve layout first, add tests/tooling incrementally | Avoid broad migration before behavior is covered. |

Package-by-feature is usually better than package-by-layer for business-heavy applications when it keeps related code together. Package-by-layer is acceptable for small apps and infrastructure-heavy projects.

## Naming And Style

- Use `lowercase` package names, normally reverse-DNS for published code.
- Use `UpperCamelCase` for classes, interfaces, enums, annotations, and records.
- Use `lowerCamelCase` for methods, fields, local variables, and parameters.
- Use `UPPER_SNAKE_CASE` for true constants.
- Avoid wildcard imports.
- Keep one public top-level type per file.
- Prefer immutable values and small constructors/factories over broad mutable objects.
- Keep framework annotations near boundaries; keep core domain code plain when practical.

## Package And API Design

- Keep public packages small and deliberate. A public class is a long-term contract in libraries.
- Use package-private classes and methods for internal collaborators.
- Prefer immutable objects for value data. Use records for transparent data carriers when appropriate.
- Prefer constructor injection for required dependencies.
- Keep static state rare and immutable.
- Avoid `Optional` fields and parameters; use it mainly for return values where absence is expected.
- Avoid checked exceptions for routine business branching; use them when the caller can recover in a meaningful way.
- Use clear domain exceptions or result types at boundaries where callers need structured failure handling.
- Keep nullability explicit through annotations if the project standard supports them.

## Build Tool Decision

| Choice | Use when | Avoid when |
| --- | --- | --- |
| Maven | Conventional library/service, simple CI, broad team familiarity | Build needs complex generated tasks or custom workflows. |
| Gradle | Multi-module builds, custom codegen, richer task graph, Android ecosystem | Team wants minimal build logic and standard Maven lifecycle. |

Do not maintain both Maven and Gradle builds for the same project unless migration is in progress. One build system should be authoritative.

## Starter Maven Plugins

For Maven projects, add tools through the build lifecycle:

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
    </plugin>
    <plugin>
      <groupId>com.diffplug.spotless</groupId>
      <artifactId>spotless-maven-plugin</artifactId>
    </plugin>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
    </plugin>
  </plugins>
</build>
```

Keep plugin versions pinned through dependency management or the build's normal version policy.

## Tooling Defaults

- Build: Maven or Gradle wrapper.
- Format: google-java-format through Spotless or the build tool.
- Static analysis: Error Prone for compiler-integrated checks; SpotBugs or Checkstyle when the project already uses them.
- Tests: JUnit 5.
- Coverage: JaCoCo when coverage gates are useful.

Recommended Maven commands:

```bash
./mvnw test
./mvnw verify
./mvnw spotless:check
```

Recommended Gradle commands:

```bash
./gradlew test
./gradlew check
./gradlew spotlessCheck
```

## Quality Gates

| Gate | Maven | Gradle | Purpose |
| --- | --- | --- | --- |
| Unit tests | `./mvnw test` | `./gradlew test` | Fast behavior tests. |
| Full verification | `./mvnw verify` | `./gradlew check` | Tests plus configured checks. |
| Format | `./mvnw spotless:check` | `./gradlew spotlessCheck` | Formatter enforcement. |
| Static analysis | Error Prone/SpotBugs/Checkstyle task | Error Prone/SpotBugs/Checkstyle task | Defect and convention checks. |
| Coverage | JaCoCo report/check | JaCoCo report/check | Coverage visibility where useful. |

Do not block early projects on arbitrary coverage percentages. Use coverage gates once the test suite is meaningful.

## TDD Guidance

- Put tests under `src/test/java` with names ending in `Test`.
- Start at the smallest public behavior: method, service, parser, repository adapter, or controller boundary.
- Use JUnit 5 assertions and parameterized tests for input matrices.
- Avoid overusing mocks. Mock external services and slow boundaries, not basic domain collaborators.
- Keep integration tests separately named when they need containers, network, or a real database.

## Test Design Details

- Use JUnit 5 assertions and lifecycle annotations.
- Name unit tests `*Test`; name slower integration tests `*IT` or put them in a separate source set according to the build tool.
- Use parameterized tests for input matrices.
- Use testcontainers or an equivalent only for integration tests that truly need real external systems.
- Avoid static global test state; it makes parallel execution fragile.
- Keep mocks at system boundaries: HTTP clients, repositories, clocks, queues, payment/email providers.
- Use fake implementations for domain collaborators when they make tests clearer than mocks.

## Service/Framework Boundary Rules

- Controllers/resources should translate HTTP/framework input into application calls and map results to responses.
- Application services orchestrate use cases and transactions.
- Domain objects enforce local invariants without framework dependencies.
- Repositories/adapters hide persistence details.
- Configuration classes wire dependencies but should contain little business logic.

This keeps the same Java structure useful across Spring, Micronaut, Quarkus, Jakarta EE, or plain Java.

## CI Baseline

Maven:

```bash
./mvnw --version
./mvnw spotless:check
./mvnw verify
```

Gradle:

```bash
./gradlew --version
./gradlew spotlessCheck
./gradlew check
```

Run with a pinned JDK version. Use toolchains when local and CI JDKs can drift.

## Review Hot Spots

- Business logic hidden in controllers, entities, annotations, or static helpers.
- Mutable DTOs passed deeply into domain code.
- N+1 query risks and lazy loading assumptions.
- Thread-unsafe shared state in singleton services.
- Catching broad `Exception` and losing context.
- Overuse of reflection, runtime magic, and annotation-only behavior without tests.
- Build logic that only works in one IDE.

## Planning Checklist

- Choose Maven or Gradle before creating files.
- Add wrapper scripts for the selected build tool.
- Add `src/main/java` and `src/test/java`.
- Add first failing JUnit 5 test.
- Add formatter and static analysis checks to local verification.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Custom source layout without need | Use standard Maven/Gradle layout. |
| Framework code throughout the domain | Keep framework boundaries thin. |
| Tests only through full application startup | Add smaller unit tests around behavior. |
| Inconsistent formatter setup across IDE and CI | Enforce formatting through the build. |
| Large utility classes | Prefer focused types with clear ownership. |
