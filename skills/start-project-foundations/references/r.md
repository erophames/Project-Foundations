# R Best Practices

Sources:
- tidyverse style guide: https://style.tidyverse.org/
- R Packages book: https://r-pkgs.org/
- testthat: https://testthat.r-lib.org/
- lintr: https://lintr.r-lib.org/
- renv: https://rstudio.github.io/renv/
- styler: https://styler.r-lib.org/
- roxygen2: https://roxygen2.r-lib.org/
- usethis: https://usethis.r-lib.org/

## Use This Reference

Apply this reference for R packages, analysis projects, data pipelines, Shiny apps, reporting projects, and scripts that need to become maintainable. R work often starts interactively; the default stance is to keep exploration possible while moving reusable behavior into tested functions.

Default stance:

- Build reusable code as an R package when it will be shared, reused, or deployed.
- Use renv for reproducible project environments.
- Use testthat for behavior tests.
- Use lintr and styler for style enforcement.
- Keep notebooks/reports as consumers of tested code, not as the only place logic exists.

## Default Structure

For reusable code, create an R package:

```text
project-name/
|-- DESCRIPTION
|-- NAMESPACE
|-- R/
|   `-- feature.R
|-- tests/
|   `-- testthat/
|       `-- test-feature.R
|-- man/
`-- README.md
```

For analysis projects, separate code, data preparation, and generated outputs:

```text
project-name/
|-- R/
|-- data-raw/
|-- tests/
|-- reports/
|-- renv.lock
`-- README.md
```

Do not commit large raw data or generated reports unless the project explicitly needs them versioned.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Package | `DESCRIPTION`, `R/`, `tests/testthat/`, `man/`, `NAMESPACE` | Best default for reusable code. |
| Analysis | `R/`, `data-raw/`, `reports/`, `tests/`, `renv.lock` | Keep generated data/reports out of source unless intentional. |
| Shiny app | `app.R` or `R/` modules plus `tests/` | Put business logic and data transforms outside server/UI glue. |
| Report pipeline | `R/`, `quarto/` or `reports/`, `data-raw/` | Render reports from tested functions. |
| Teaching/exploration | notebooks/scripts plus gradual extraction to `R/` | Do not over-package throwaway work. |

Avoid `helpers.R` as a first shared file. Prefer `read_sales.R`, `clean_customers.R`, `fit_forecast.R`.

## Naming And Style

- Use `snake_case` for functions, variables, file names, and object names.
- Use function names that start with verbs when they perform actions.
- Use clear nouns for data objects.
- Avoid dots in new function names unless implementing S3 methods.
- Prefer explicit returns only when they improve readability.
- Keep pipe chains readable; extract named intermediate values when chains become hard to debug.
- Avoid hidden global state in scripts; pass inputs as arguments.

## Function And Data Design

- Write functions that accept data and configuration as arguments and return values.
- Keep side effects at the edges: reading files, writing outputs, plotting, network calls, database calls.
- Use tibbles/data frames consistently and document required columns for public functions.
- Validate required columns and types at function boundaries.
- Prefer explicit namespace calls for less-common package functions in reusable code.
- Avoid `library()` inside package code; declare dependencies in `DESCRIPTION`.
- Use S3 methods intentionally and follow naming conventions when implementing them.
- Keep random operations reproducible by accepting a seed or RNG state at the boundary.
- Return errors with actionable messages that mention the argument or column causing the failure.

## Package Metadata Defaults

`DESCRIPTION` should include:

```text
Package: projectname
Title: Short Title in Title Case
Version: 0.1.0
Authors@R:
    person("First", "Last", , "email@example.com", role = c("aut", "cre"))
Description: One paragraph describing what the package does.
License: MIT + file LICENSE
Encoding: UTF-8
Roxygen: list(markdown = TRUE)
RoxygenNote: 7.3.0
Suggests:
    testthat (>= 3.0.0)
Config/testthat/edition: 3
```

Add imports only for packages used by package code. Keep analysis-only packages in project tooling or suggests where appropriate.

## Reproducibility Policy

- Use `renv::init()` for analysis projects, Shiny apps, and report pipelines.
- Commit `renv.lock` when reproducibility matters.
- Keep large raw data outside git; commit small fixtures under `tests/testthat/fixtures/` or `inst/extdata/` only when useful.
- Record data provenance in `data-raw/` scripts or project docs.
- Never rely on interactive global environment objects in scripts that others must run.
- Use relative paths from the project root through `here` or an equivalent project-root convention.

## Tooling Defaults

- Dependency isolation: renv.
- Package workflow: usethis/devtools.
- Tests: testthat.
- Lint: lintr.
- Format: styler.
- Documentation: roxygen2 for package APIs.

Recommended commands:

```bash
R CMD check .
Rscript -e 'testthat::test_dir("tests/testthat")'
Rscript -e 'lintr::lint_package()'
Rscript -e 'styler::style_pkg(dry = "on")'
```

Use `devtools::check()` during interactive package development if that is the local team workflow.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Package check | `R CMD check .` | Packaging, docs, examples, tests. |
| Unit tests | `Rscript -e 'testthat::test_dir("tests/testthat")'` | Fast behavior loop. |
| Lint | `Rscript -e 'lintr::lint_package()'` | Style and static checks for packages. |
| Style dry run | `Rscript -e 'styler::style_pkg(dry = "on")'` | Formatting check. |
| renv status | `Rscript -e 'renv::status()'` | Dependency lock consistency. |

For non-package analysis projects, replace package-specific commands with `lint_dir()`, targeted testthat calls, and a render/smoke command for reports.

## TDD Guidance

- Put package tests under `tests/testthat`.
- Name tests by behavior: `test-normalize-email.R`.
- Test functions with small data frames that cover missing values, types, grouping, and empty input.
- For analysis projects, test transformation functions rather than rendered reports.
- Keep random behavior reproducible with explicit seeds at test boundaries.

## Test Design Details

- Test transformations with small in-memory data frames.
- Cover empty data, missing values, duplicate keys, unexpected factor/character levels, and grouped data.
- Use snapshots sparingly for printed output; prefer explicit expectations for data.
- Use fixtures for stable file formats, but keep them small.
- Test warnings and errors with testthat expectations when they are part of the contract.
- Avoid tests that depend on local package libraries outside renv.
- For Shiny, test server logic and modules separately from full browser automation when possible.

## Analysis Workflow Rules

- Exploration can happen in notebooks/scripts, but reusable steps move into `R/`.
- `data-raw/` scripts create documented intermediate or package data.
- Reports should call functions rather than duplicate transformation logic.
- Plots used in reports should be generated by functions with clear inputs.
- Keep cache directories and generated output ignored unless they are explicit deliverables.
- Make long-running analysis steps restartable.

## CI Baseline

Package:

```bash
R CMD check .
Rscript -e 'lintr::lint_package()'
Rscript -e 'styler::style_pkg(dry = "on")'
```

Analysis project:

```bash
Rscript -e 'renv::restore()'
Rscript -e 'testthat::test_dir("tests")'
Rscript -e 'lintr::lint_dir("R")'
```

Add report rendering only when the project has reports as deliverables.

## Review Hot Spots

- Logic only in notebooks or top-level scripts.
- Hidden reliance on global variables.
- Unpinned dependencies for reproducible analysis.
- Large data committed without intent.
- Tests that depend on local absolute paths.
- Overly long pipe chains that hide intermediate assumptions.
- Silent recycling or implicit type conversion in data transforms.

## Planning Checklist

- Decide package vs analysis project vs Shiny app.
- Add renv when reproducibility matters.
- Add first failing testthat test.
- Add lintr and styler checks.
- Add package documentation if functions are public.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Production logic only in notebooks or scripts | Extract functions into `R/` and test them. |
| Unpinned package versions for analysis | Use renv for reproducibility. |
| Large implicit globals | Pass data and configuration explicitly. |
| Tests depend on local files outside the repo | Use fixtures or generated temporary data. |
| Overlong pipe chains | Split into named steps when debugging cost rises. |
