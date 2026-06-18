# Scala Best Practices

Sources:
- Scala style guide: https://docs.scala-lang.org/style/
- Scala 3 book: https://docs.scala-lang.org/scala3/book/introduction.html
- sbt reference manual: https://www.scala-sbt.org/1.x/docs/index.html
- scalafmt: https://scalameta.org/scalafmt/
- ScalaTest user guide: https://www.scalatest.org/user_guide

## Use This Reference

Apply this reference when Scala owns a JVM library, service, data job, CLI, Spark application, Akka/Pekko app, or mixed Java/Scala module. Scala projects should be explicit about style, effects, build boundaries, and testing. Avoid mixing every Scala paradigm at once; choose a pragmatic project style and keep it consistent.

Default stance:

- Use sbt unless the repository standard is Maven/Gradle.
- Use standard `src/main/scala` and `src/test/scala` layout.
- Use scalafmt and ScalaTest or MUnit.
- Prefer Scala 3 for new projects unless dependency/tooling constraints require Scala 2.
- Keep Java interop explicit and avoid clever type-level design unless it clearly improves safety.

## Default Structure

```text
project-name/
|-- build.sbt
|-- project/
|   |-- build.properties
|   `-- plugins.sbt
|-- .scalafmt.conf
|-- src/
|   |-- main/
|   |   `-- scala/
|   |       `-- com/example/project/
|   `-- test/
|       `-- scala/
|           `-- com/example/project/
`-- README.md
```

For multi-module builds, use subprojects in `build.sbt` and keep shared settings in a small helper object under `project/`.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Library | `src/main/scala`, `src/test/scala` | Keep public API stable and documented. |
| Service | app/domain/adapters packages | Keep HTTP/framework layer thin. |
| CLI | main object plus testable command module | Keep parsing separate from behavior. |
| Spark/data job | jobs, schemas, transforms, integration tests | Keep transformations pure where possible. |
| Multi-module | sbt subprojects | Use when dependency or deployment boundaries are real. |
| Mixed Java/Scala | Shared JVM layout | Keep nullability and collection conversion explicit. |

## Naming And Style

- Use `UpperCamelCase` for classes, traits, objects, and type aliases.
- Use `lowerCamelCase` for methods, values, variables, and parameters.
- Use `SCREAMING_SNAKE_CASE` rarely; prefer ordinary `val` names unless matching Java constants.
- Use package names in lowercase.
- Keep symbolic method names rare and domain-justified.
- Use scalafmt as the formatting authority.
- Prefer descriptive names over abbreviations.
- Keep imports organized by the formatter/tooling convention.

## API And Type Design

- Use immutable values by default: `val` over `var`.
- Prefer case classes for immutable data carriers.
- Use sealed traits/enums for closed algebraic data types.
- Use `Option` instead of nullable values in Scala-owned APIs.
- Use `Either`, `Try`, or an effect type for recoverable failures according to project style.
- Avoid throwing exceptions through pure/domain APIs unless Java interop or framework contracts require it.
- Keep implicits/givens local, named clearly, and documented when public.
- Avoid typeclass or macro-heavy abstractions until they simplify real duplication or safety problems.
- Keep side effects at boundaries and explicit in service/data jobs.

## sbt And Dependency Policy

- Pin sbt version in `project/build.properties`.
- Keep dependencies in one readable place for small projects.
- Use multi-project builds only for real boundaries.
- Avoid global plugins or developer-local sbt settings as build requirements.
- Keep Scala binary version compatibility in mind for libraries.
- Use dependency eviction/conflict checks in mature services.

Starter `build.sbt` shape:

```scala
ThisBuild / scalaVersion := "3.7.0"

lazy val root = (project in file("."))
  .settings(
    name := "project-name",
    libraryDependencies += "org.scalatest" %% "scalatest" % "3.2.19" % Test
  )
```

Adjust versions to the selected runtime and dependency ecosystem.

## Tooling Defaults

Recommended commands:

```bash
sbt scalafmtCheckAll
sbt compile
sbt test
sbt package
```

Common additions:

- `scalafix` for semantic rewrites/linting where configured.
- `sbt-assembly` only when fat JAR packaging is required.
- `wartremover` or compiler warnings when the team accepts stricter style.

## Testing And TDD

- Put tests under `src/test/scala`.
- Start with one failing test for a pure function, parser, service method, repository adapter, or job transformation.
- Use ScalaTest, MUnit, or specs2 consistently.
- Prefer testing pure transformations without Spark/framework runtime when possible.
- Test Java interop nulls, failed futures/effects, empty collections, and pattern-match exhaustiveness.
- Use property tests for algebraic/domain invariants when input space is broad.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Format | `sbt scalafmtCheckAll` | Enforces formatting. |
| Compile | `sbt compile` | Verifies main sources. |
| Tests | `sbt test` | Runs unit/integration tests. |
| Package | `sbt package` | Confirms artifact creation. |
| Warnings | `sbt -Wconf... compile` or configured strict warnings | Prevents ignored compiler feedback. |

## CI Baseline

```bash
java -version
sbt --version
sbt scalafmtCheckAll
sbt compile
sbt test
sbt package
```

Cache Ivy/Coursier and sbt directories carefully. For libraries, test supported Scala versions when cross-publishing.

## Security And Robustness

- Validate external input before constructing domain values.
- Avoid blocking calls inside async/effect runtimes.
- Treat Java nulls and exceptions explicitly at interop boundaries.
- Keep config parsing typed and fail fast.
- Avoid unbounded collection loads in services/data jobs.
- Keep secrets out of logs and case-class `toString` output.

## Review Hot Spots

- Over-abstracted type-level code hiding simple behavior.
- Implicits/givens imported broadly and changing behavior invisibly.
- `var`, mutable collections, and side effects in domain code.
- Blocking operations in futures/effects.
- Pattern matches that are not exhaustive.
- Spark jobs with untested transformations.
- Multi-module builds split before boundaries are useful.
