# PHP Best Practices

Sources:
- PHP Standards Recommendations: https://www.php-fig.org/psr/
- Composer introduction: https://getcomposer.org/doc/00-intro.md
- PHPUnit manual: https://docs.phpunit.de/en/12.2/index.html
- PHPStan getting started: https://phpstan.org/user-guide/getting-started
- Psalm installation: https://psalm.dev/docs/running_psalm/installation/

## Use This Reference

Apply this reference when PHP owns the project: a package, CLI, web app, API, Laravel/Symfony app, WordPress plugin, migration, or legacy modernization. PHP projects should use Composer, PSR conventions, automated tests, and static analysis. Framework defaults are valuable, but domain code should still be separated, typed, and testable.

Default stance:

- Use Composer for dependency management and autoloading.
- Follow PSR-12 style for new non-framework code.
- Use namespaces and PSR-4 autoloading.
- Use PHPUnit by default; Pest is acceptable when the team prefers it.
- Use PHPStan or Psalm for static analysis.
- Use framework layout when using Laravel, Symfony, or another established framework.

## Default Structure

For a library/package:

```text
project-name/
|-- composer.json
|-- src/
|   `-- ProjectName/
|       `-- Service.php
|-- tests/
|   `-- ServiceTest.php
|-- phpunit.xml.dist
|-- phpstan.neon
`-- README.md
```

For a framework app, start from the framework generator and keep custom domain/application code in explicit services, actions, jobs, or modules rather than burying it in controllers.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Composer package | `src/`, `tests/`, `composer.json` | Use PSR-4 and clear public API. |
| CLI | `bin/name`, `src/Command`, `tests/` | Keep command IO thin and behavior testable. |
| Web/API app | Framework default plus domain services | Keep controllers thin and validate request DTOs. |
| WordPress plugin | Plugin entrypoint plus `src/` | Isolate hooks from domain behavior. |
| Legacy migration | Existing layout plus Composer/test harness | Add autoloading and tests incrementally. |

## Naming And Style

- Use `PascalCase` for classes, interfaces, traits, and enums.
- Use `camelCase` for methods, functions, properties, variables, and parameters.
- Use `UPPER_SNAKE_CASE` for constants.
- Use one class per file under a namespace matching PSR-4 autoloading.
- Prefer strict types at file top in new code:

  ```php
  declare(strict_types=1);
  ```

- Add return types and parameter types for public APIs.
- Use nullable and union types deliberately; do not hide uncertain input behind `mixed`.
- Keep PHPDoc for generics, array shapes, templates, or value constraints that PHP types cannot express.

## API And Application Design

- Keep controllers, route handlers, hooks, and command classes thin.
- Put business behavior in services, actions, domain objects, or framework-appropriate equivalents.
- Use value objects for IDs, money, dates, and state when primitive mixing is risky.
- Throw domain-specific exceptions only when callers can handle them.
- Prefer dependency injection over service locators for testable code.
- Keep global functions rare outside small procedural plugins or compatibility layers.
- Validate external input at request/CLI/message boundaries.
- Avoid static state unless it wraps a true constant or framework-required integration.

## Composer And Dependency Policy

- Define `require`, `require-dev`, `autoload`, and `autoload-dev` explicitly.
- Commit `composer.lock` for applications and services.
- Libraries may commit `composer.lock` for CI reproducibility, but consumers resolve their own dependency graph.
- Keep PHP version constraints realistic and tested.
- Use scripts for standard checks:

  ```json
  {
    "scripts": {
      "test": "phpunit",
      "analyse": "phpstan analyse",
      "check": [
        "@test",
        "@analyse"
      ]
    }
  }
  ```

- Avoid adding large framework dependencies to small packages.

## Tooling Defaults

Recommended commands:

```bash
composer validate --strict
composer install
vendor/bin/phpunit
vendor/bin/phpstan analyse
vendor/bin/psalm
composer audit
```

Use either PHPStan or Psalm as the default static analyzer unless the project benefits from both. Add PHP-CS-Fixer or Pint when the repo wants automated formatting; otherwise enforce PSR-12 through the existing framework/tooling.

## Testing And TDD

- Put tests under `tests/` and name them `*Test.php`.
- Start with one failing test against a public method, command behavior, request handler, or domain service.
- Use PHPUnit data providers for small input matrices.
- Prefer real value objects and in-memory/fake adapters over broad mocks.
- Test exceptions, validation failures, null/empty inputs, and boundary conversions.
- For framework apps, test domain services separately from HTTP/controller tests.
- For database code, separate fast unit tests from integration tests that require a real database.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Composer metadata | `composer validate --strict` | Validates package metadata and autoload config. |
| Tests | `vendor/bin/phpunit` | Runs behavior/regression tests. |
| Static analysis | `vendor/bin/phpstan analyse` or `vendor/bin/psalm` | Finds type and flow defects. |
| Dependencies | `composer audit` | Checks known dependency vulnerabilities. |
| Framework check | Framework-specific command | Confirms config/container/routes compile. |

For Laravel, include `php artisan test` and Pint if configured. For Symfony, include container linting and PHPUnit through the project recipe.

## CI Baseline

```bash
php -v
composer validate --strict
composer install --no-interaction --prefer-dist
vendor/bin/phpunit
vendor/bin/phpstan analyse
composer audit
```

Run a PHP version matrix for libraries. Keep extensions explicit in Composer and CI setup.

## Security And Robustness

- Use prepared statements or framework query builders for database input.
- Escape output according to context: HTML, attribute, URL, shell, JSON.
- Do not deserialize untrusted PHP objects.
- Avoid dynamic includes from user-controlled paths.
- Keep secrets out of `.env` examples and logs.
- Validate uploaded files by content and destination, not just extension.
- Use constant-time comparison for secrets/tokens when available.

## Review Hot Spots

- Missing `strict_types`, weak `mixed`, and untyped public APIs.
- Controllers or hooks containing business logic.
- Raw SQL or shell calls with interpolated user input.
- Composer autoload mismatches.
- Static facades/globals hiding dependencies from tests.
- Tests that require production services by default.
- Suppressed static-analysis findings without narrow justification.
