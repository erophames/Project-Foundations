# SQL Best Practices

Sources:
- SQL style guide by Simon Holywell: https://www.sqlstyle.guide/
- SQLFluff documentation: https://docs.sqlfluff.com/
- dbt best practices: https://docs.getdbt.com/best-practices
- Flyway migrations: https://documentation.red-gate.com/fd/migrations-184127470.html
- Liquibase concepts: https://docs.liquibase.com/concepts/home.html
- PostgreSQL documentation: https://www.postgresql.org/docs/current/
- SQLite documentation: https://www.sqlite.org/docs.html
- Microsoft T-SQL documentation: https://learn.microsoft.com/en-us/sql/t-sql/language-reference

## Use This Reference

Apply this reference when SQL itself is a primary project artifact: migrations, stored procedures, analytical models, dbt projects, warehouse transforms, database test suites, or application query libraries. Always identify the target dialect before making strong style or tooling decisions. SQL is not portable enough to treat dialect as an afterthought.

Default stance:

- Use migrations for application schema changes.
- Use dbt-style structure for analytical transformations when dbt is selected.
- Use SQLFluff with the actual dialect configured.
- Test against the target database or the closest supported local equivalent.
- Keep generated dumps, scratch queries, and local database files out of source control unless they are intentional fixtures.

## Default Structure

For application database changes:

```text
project-name/
`-- db/
    |-- migrations/
    |-- seeds/
    |-- views/
    |-- tests/
    `-- .sqlfluff
```

For dbt analytics projects, use dbt defaults:

```text
project-name/
|-- dbt_project.yml
|-- models/
|   |-- staging/
|   |-- intermediate/
|   `-- marts/
|-- macros/
|-- seeds/
`-- tests/
```

Keep generated dumps, local database files, and one-off scratch queries out of versioned source directories unless they are intentional fixtures.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| App migrations | `db/migrations/`, `db/seeds/`, `db/tests/` | Use the application's migration tool when one exists. |
| dbt analytics | `models/staging/`, `models/intermediate/`, `models/marts/`, `tests/`, `macros/` | Follow dbt's structure/style guidance and add schema tests. |
| Stored procedures | `db/procedures/`, `db/functions/`, `db/tests/` | Version definitions and add deploy/revert scripts if tooling lacks migrations. |
| Query library | `sql/queries/`, `tests/sql/`, app fixtures | Keep parameterized query files near the app code that owns them when possible. |
| Data warehouse | `models/`, `snapshots/`, `seeds/`, environment profiles | Separate source-shaped staging from business-shaped marts. |

Migration filenames should include order and intent, for example `V20260618_001__create_accounts.sql` or `202606181430_create_accounts.sql`, depending on the migration tool.

## Naming And Style

- Use `snake_case` for schemas, tables, columns, CTEs, and aliases.
- Avoid quoted identifiers unless the database requires them.
- Avoid reserved words as object names.
- Use a consistent keyword style and enforce it with SQLFluff. A practical default is uppercase SQL keywords and lowercase identifiers.
- Prefer explicit column lists over `SELECT *` outside exploratory work.
- Use readable CTEs for multi-step transformations, with one logical step per CTE.
- Name migrations so ordering and intent are obvious.

## Dialect Decisions

Capture these before writing SQL:

- Engine and version: PostgreSQL, MySQL/MariaDB, SQLite, SQL Server, Oracle, BigQuery, Snowflake, Redshift, DuckDB, Spark SQL, Trino, or other.
- Deployment model: application migrations, DBA-managed scripts, dbt, warehouse jobs, or stored procedure deployment.
- Transaction semantics: whether DDL is transactional for the target engine.
- Identifier casing behavior: especially SQL Server, PostgreSQL, and warehouses with quoted identifiers.
- Time zone rules: what type represents instants vs local dates.
- JSON/array support: native types vs text columns.
- Migration rollback policy: reversible migration, forward fix, backup/restore, or manual runbook.

Do not use SQLite as a stand-in for PostgreSQL/MySQL/SQL Server behavior when the feature depends on types, constraints, transactions, query planner behavior, or concurrency.

## SQL Style Details

- Prefer stable column ordering: identifiers, foreign keys, required attributes, optional attributes, timestamps, metadata.
- Use explicit join types: `INNER JOIN`, `LEFT JOIN`, etc.
- Put join predicates in `ON`, not `WHERE`, unless intentionally filtering after an outer join.
- Use table aliases that improve readability, not one-letter aliases everywhere.
- Avoid ordinal `GROUP BY 1` / `ORDER BY 1` in production SQL.
- Avoid implicit casts at critical boundaries; cast intentionally and visibly.
- Use `NULL` intentionally. Add tests for null-heavy inputs.
- Use constraints as executable documentation: `NOT NULL`, `UNIQUE`, `CHECK`, foreign keys, and indexes where supported.
- Avoid storing comma-separated lists in text columns. Model relationships explicitly or use a native array/JSON type only when that is the right query shape.

## Starter `.sqlfluff`

```ini
[sqlfluff]
dialect = postgres
templater = raw
max_line_length = 100

[sqlfluff:layout:type:comma]
line_position = trailing

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = upper

[sqlfluff:rules:capitalisation.identifiers]
extended_capitalisation_policy = lower
```

Change `dialect` before writing queries. Use the dbt templater only inside dbt projects; raw SQL projects should not pay for dbt-specific parsing.

## Tooling Defaults

- Lint/format: SQLFluff with the target dialect configured.
- Migrations: Flyway, Liquibase, Rails/Django migrations, or the application's existing migration tool.
- Analytics: dbt for model/test/build workflows.
- Verification: run SQL against the target engine or a close local equivalent; SQL is dialect-sensitive.

Recommended commands:

```bash
sqlfluff lint db/
sqlfluff fix --check db/
dbt build
```

Use migration-tool dry runs or a disposable database for schema changes.

## Quality Gates

| Gate | Default command | Purpose |
| --- | --- | --- |
| Lint | `sqlfluff lint db/` | Style, parseability, common query defects. |
| Format check | `sqlfluff fix --check db/` or `sqlfluff format --check db/` | Confirms SQL formatting is stable. |
| Migration apply | tool-specific migrate command against disposable DB | Proves schema changes run from empty state. |
| Migration compatibility | apply against representative existing data | Proves production-like upgrade path. |
| dbt build | `dbt build` | Runs models, tests, snapshots, and seeds as configured. |
| Explain/perf check | database-specific `EXPLAIN` | Required for hot paths and large transforms. |

For application queries, add app-level tests that execute the query with fixtures. For warehouse SQL, add data tests for uniqueness, not-null, accepted values, relationships, and business invariants.

## TDD Guidance

- Start with a failing migration/model/query test before changing schema or transformation logic.
- For migrations, test forward migration on an empty database and representative existing data.
- For dbt, add schema tests for uniqueness, not-null, relationships, and accepted values.
- For application queries, use small fixtures and verify result shape, ordering, and edge cases.
- Always include rollback or recovery thinking, even when the tool does not support automatic rollback.

## Migration Guidance

- Make each migration one coherent schema change.
- Prefer additive changes for zero-downtime deployments: add nullable column, backfill, deploy app read/write compatibility, enforce constraint later.
- Avoid long exclusive locks in high-traffic tables. Plan indexes and backfills with the engine's online/concurrent options.
- Never edit an already-applied migration in shared environments. Add a new migration.
- Keep seed data deterministic and idempotent when the migration tool supports it.
- Keep destructive migrations explicit and reviewed: drops, truncates, irreversible type changes, mass updates.
- Include data cleanup in controlled, tested migrations rather than one-off manual queries.

## Query Review Checklist

- Are predicates sargable for the target engine?
- Are joins using the intended cardinality?
- Are nulls handled intentionally?
- Is ordering deterministic when callers depend on order?
- Are time zones explicit?
- Are indexes aligned with filters, joins, and constraints?
- Are permissions and ownership considered for views/procedures?
- Is the query safe with empty input, duplicate rows, and unexpected casing/whitespace?

## CI Baseline

Application SQL:

```bash
sqlfluff lint db/
# apply migrations to disposable database
# run application query/integration tests
```

dbt SQL:

```bash
sqlfluff lint models/ macros/ tests/
dbt deps
dbt build
```

Keep production credentials out of CI. Use disposable databases, temporary schemas, or warehouse-specific CI datasets.

## Planning Checklist

- Identify dialect: PostgreSQL, MySQL, SQLite, SQL Server, Oracle, BigQuery, Snowflake, DuckDB, or other.
- Choose migration project vs dbt analytics project vs application query organization.
- Add SQLFluff dialect/config.
- Add first failing database/model/query test.
- Add disposable database or warehouse-safe verification path.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Writing dialect-neutral SQL without testing a dialect | Configure tools and tests for the actual engine. |
| `SELECT *` in production queries | List columns explicitly. |
| Unordered result tests | Assert ordering when order matters. |
| Migrations not tested on existing data shapes | Test representative pre-migration data. |
| Names that require quoting forever | Use simple `snake_case` identifiers. |
