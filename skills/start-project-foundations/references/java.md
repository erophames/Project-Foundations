# Java Best Practices

Sources:
- Google Java Style Guide: https://google.github.io/styleguide/javaguide.html
- Maven standard directory layout: https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html
- Maven POM properties: https://maven.apache.org/pom.html#Properties
- Gradle Java plugin: https://docs.gradle.org/current/userguide/java_plugin.html
- JUnit 5 user guide: https://junit.org/junit5/docs/current/user-guide/
- Error Prone: https://errorprone.info/
- NullAway: https://github.com/uber/NullAway
- Spotless: https://github.com/diffplug/spotless
- JaCoCo: https://www.jacoco.org/jacoco/trunk/doc/
- SpotBugs: https://spotbugs.github.io/
- Checkstyle: https://checkstyle.org/
- PMD: https://pmd.github.io/
- Modernizer Maven Plugin: https://github.com/gaul/modernizer-maven-plugin
- ArchUnit: https://www.archunit.org/
- OWASP Dependency-Check Maven Plugin: https://jeremylong.github.io/DependencyCheck/dependency-check-maven/
- Tidy Maven Plugin: https://github.com/jingboy/tidy-maven-plugin
- Maven Versions Plugin: https://www.mojohaus.org/versions/versions-maven-plugin/
- JetBrains Annotations (@Nullable/@NotNull): https://github.com/JetBrains/java-annotations

## Use This Reference

Apply this reference for Java libraries, CLIs, services, JVM applications, Android-adjacent pure Java modules, and framework projects where Java is the primary language. Framework-specific conventions can add structure, but they should not erase the standard Maven/Gradle source layout or the separation between domain logic and framework glue.

Default stance:

- Use standard Maven/Gradle source layout.
- Pick Maven for conventional/simple builds and Gradle for builds that need richer customization.
- Manage all dependency and plugin versions through POM `<properties>` — no hardcoded versions scattered across plugin configuration.
- Add wrapper scripts for reproducible local and CI execution.
- Use JUnit 5 for tests.
- Enforce formatting in the build, not only in IDE settings.
- Run the full quality gate set in every CI build: format, lint, static analysis, architecture tests, coverage, security scan, and dependency freshness checks.

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
- Keep nullability explicit through JetBrains `@Nullable`/`@NotNull` annotations on all public API surfaces, enforced by NullAway at compile time.

## Build Tool Decision

| Choice | Use when | Avoid when |
| --- | --- | --- |
| Maven | Conventional library/service, simple CI, broad team familiarity | Build needs complex generated tasks or custom workflows. |
| Gradle | Multi-module builds, custom codegen, richer task graph, Android ecosystem | Team wants minimal build logic and standard Maven lifecycle. |

Do not maintain both Maven and Gradle builds for the same project unless migration is in progress. One build system should be authoritative.

## Starter Maven Plugins

For Maven projects, add the full quality stack through the build lifecycle. Define every version as a `<property>` so upgrades stay in one place:

```xml
<properties>
  <maven.compiler.release>21</maven.compiler.release>
  <checkstyle.version>10.18.0</checkstyle.version>
  <error-prone.version>2.31.0</error-prone.version>
  <nullaway.version>0.11.0</nullaway.version>
  <spotbugs.version>4.8.6</spotbugs.version>
  <spotbugs.plugin.version>4.8.6.5</spotbugs.plugin.version>
  <pmd.version>3.24.0</pmd.plugin.version>
  <spotless.version>2.43.0</spotless.version>
  <modernizer.version>2.9.0</modernizer.version>
  <jacoco.version>0.8.12</jacoco.version>
  <archunit.version>1.3.0</archunit.version>
  <owasp.dc.version>10.0.4</owasp.dc.version>
  <tidy.version>1.2.0</tidy.version>
  <versions.plugin.version>2.17.1</versions.plugin.version>
</properties>

<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
    </plugin>
    <plugin>
      <groupId>com.diffplug.spotless</groupId>
      <artifactId>spotless-maven-plugin</artifactId>
      <version>${spotless.version}</version>
    </plugin>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>${jacoco.version}</version>
    </plugin>
    <plugin>
      <groupId>com.github.spotbugs</groupId>
      <artifactId>spotbugs-maven-plugin</artifactId>
      <version>${spotbugs.plugin.version}</version>
    </plugin>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-checkstyle-plugin</artifactId>
    </plugin>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-pmd-plugin</artifactId>
    </plugin>
    <plugin>
      <groupId>org.gaul</groupId>
      <artifactId>modernizer-maven-plugin</artifactId>
      <version>${modernizer.version}</version>
    </plugin>
    <plugin>
      <groupId>net.jingboy.maven.plugins</groupId>
      <artifactId>tidy-maven-plugin</artifactId>
      <version>${tidy.version}</version>
    </plugin>
    <plugin>
      <groupId>org.owasp</groupId>
      <artifactId>dependency-check-maven</artifactId>
      <version>${owasp.dc.version}</version>
    </plugin>
    <plugin>
      <groupId>org.codehaus.mojo</groupId>
      <artifactId>versions-maven-plugin</artifactId>
      <version>${versions.plugin.version}</version>
    </plugin>
  </plugins>
</build>
```

For Error Prone with NullAway, configure the compiler annotation processor:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <compilerArgs>
      <arg>-Xplugin:ErrorProne</arg>
      <arg>-Xep:NullAway:ERROR</arg>
      <arg>-XepOpt:NullAway:AnnotatedPackages=com.example.project</arg>
    </compilerArgs>
    <annotationProcessorPaths>
      <path>
        <groupId>com.google.errorprone</groupId>
        <artifactId>error_prone_core</artifactId>
        <version>${error-prone.version}</version>
      </path>
      <path>
        <groupId>com.uber.nullaway</groupId>
        <artifactId>nullaway</artifactId>
        <version>${nullaway.version}</version>
      </path>
    </annotationProcessorPaths>
  </configuration>
</plugin>
```

Keep plugin versions pinned through `<properties>` so a single property update propagates everywhere.

## Tooling Defaults

- Build: Maven or Gradle wrapper.
- Format: google-java-format through Spotless.
- Static analysis — mandatory:
  - Error Prone with NullAway for null-safety enforcement at compile time.
  - Checkstyle for style and convention enforcement.
  - PMD for code defect and copy-paste detection.
  - SpotBugs for bug pattern detection.
  - Modernizer Maven Plugin for detecting use of legacy/concurrent APIs that have modern replacements.
- Architecture testing: ArchUnit for enforcing layering, package dependency rules, and cycle detection.
- Coverage: JaCoCo with threshold enforcement once the suite is meaningful.
- Security: OWASP Dependency-Check for transitive dependency vulnerability scanning.
- Dependency hygiene: Tidy Maven Plugin for POM normalization and versions-maven-plugin for update detection.
- Nullability: JetBrains `@Nullable`/`@NotNull` annotations at API boundaries, enforced by NullAway.
- Tests: JUnit 5.

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
| Static analysis | Error Prone + NullAway | Error Prone + NullAway | Compile-time null-safety and bug detection. |
| Style | `./mvnw checkstyle:check` | Checkstyle task | Convention enforcement. |
| Code defects | `./mvnw pmd:check` | PMD task | Defect and copy-paste detection. |
| Bug patterns | `./mvnw spotbugs:check` | SpotBugs task | Bug pattern detection. |
| Modernization | `./mvnw modernizer:modernizer` | Modernizer task | Legacy API detection. |
| Architecture | ArchUnit test suite (`./mvnw test`) | ArchUnit test suite (`./gradlew test`) | Layer and dependency rule enforcement. |
| Coverage | JaCoCo report/check | JaCoCo report/check | Coverage visibility where useful. |
| Security | `./mvnw dependency-check:check` | OWASP dependency-check task | Transitive CVE scanning. |
| POM hygiene | `./mvnw tidy:check` | N/A (Maven only) | POM normalization and formatting. |
| Dependency freshness | `./mvnw versions:display-dependency-updates` | versions task | Detect outdated dependencies. |

Do not block early projects on arbitrary coverage percentages. Use coverage gates once the test suite is meaningful. Security and architecture gates should be active from the first commit.

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
./mvnw tidy:check
./mvnw spotless:check
./mvnw checkstyle:check
./mvnw pmd:check
./mvnw spotbugs:check
./mvnw modernizer:modernizer
./mvnw verify
./mvnw dependency-check:check
./mvnw versions:display-dependency-updates
```

Gradle:

```bash
./gradlew --version
./gradlew spotlessCheck
./gradlew check
```

Run with a pinned JDK version. Use toolchains when local and CI JDKs can drift.

## Architecture Testing

Use ArchUnit to enforce architectural rules as executable tests that fail the build when violated:

- **Layer dependencies:** domain must not depend on infrastructure or web layers.
- **Package cycles:** no cyclic dependencies between packages.
- **Naming conventions:** controllers must end in `Controller`, repositories in `Repository`.
- **Framework isolation:** domain packages must not import Spring/Jakarta/ framework types.

ArchUnit tests live alongside regular unit tests in `src/test/java` and run as part of `./mvnw test` or `./gradlew test`. Treat architecture violations as build failures, not warnings.

## Nullability Annotations

Use JetBrains annotations (`@Nullable`, `@NotNull`) or JSR-305 (`@CheckForNull`) consistently at API boundaries:

- Annotate method parameters, return types, and fields on public API surfaces.
- Configure NullAway with `-XepOpt:NullAway:AnnotatedPackages=com.example.project` to match the project's root package.
- Treat NullAway violations as compile errors, not warnings.
- Do not rely on annotations alone for documentation; pair with `Optional` returns where absence is a normal, expected path.

## Security And Dependency Scanning

- Run OWASP Dependency-Check in every CI build to catch known CVEs in transitive dependencies.
- Use the versions-maven-plugin to detect outdated dependencies regularly.
- Use Tidy Maven Plugin to keep the POM normalized (sorted dependencies, consistent formatting, no unused elements).
- Fail the build on CVSS score above the project threshold (e.g., `failBuildOnAnyVulnerability` or `suppressionFile` for accepted risks).

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
- Define all plugin and dependency versions in POM `<properties>`.
- Add `src/main/java` and `src/test/java`.
- Add first failing JUnit 5 test.
- Add formatter (Spotless) and static analysis checks (Error Prone + NullAway, Checkstyle, PMD, SpotBugs, Modernizer) to local verification.
- Add ArchUnit tests for layer and package dependency rules.
- Add JaCoCo coverage reporting.
- Add OWASP Dependency-Check and versions-maven-plugin to CI.
- Add Tidy Maven Plugin for POM hygiene (Maven only).
- Add JetBrains `@Nullable`/`@NotNull` annotations to public API boundaries.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Custom source layout without need | Use standard Maven/Gradle layout. |
| Framework code throughout the domain | Keep framework boundaries thin. |
| Tests only through full application startup | Add smaller unit tests around behavior. |
| Inconsistent formatter setup across IDE and CI | Enforce formatting through the build. |
| Large utility classes | Prefer focused types with clear ownership. |
