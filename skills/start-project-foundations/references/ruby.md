# Ruby Best Practices

Sources:
- RubyGems/Bundler getting started: https://guides.rubygems.org/getting_started/
- Make your own gem: https://guides.rubygems.org/make-your-own-gem/
- Ruby on Rails getting started: https://guides.rubyonrails.org/getting_started.html
- RSpec documentation: https://rspec.info/documentation/
- RuboCop documentation: https://docs.rubocop.org/rubocop/1.77/index.html

## Use This Reference

Apply this reference when Ruby owns a gem, CLI, Rails app, service, script collection, automation task, or legacy Ruby/Rails modernization. Ruby projects should use Bundler, clear object boundaries, tests, and RuboCop. Rails conventions are strong defaults for Rails apps, but domain behavior should remain testable without full request/browser flows.

Default stance:

- Use Bundler and commit `Gemfile.lock` for applications.
- Use gem skeleton conventions for libraries.
- Use RuboCop for style and maintainability.
- Use RSpec or Minitest consistently; Rails default Minitest is fine unless the team prefers RSpec.
- Keep Rails controllers, jobs, and callbacks thin.
- Pin Ruby version with `.ruby-version` or the repo's standard version manager.

## Default Structure

For a gem:

```text
project-name/
|-- project-name.gemspec
|-- Gemfile
|-- lib/
|   |-- project_name.rb
|   `-- project_name/
|       `-- feature.rb
|-- spec/
|   `-- project_name_spec.rb
`-- README.md
```

For a small CLI:

```text
project-name/
|-- Gemfile
|-- exe/
|   `-- project-name
|-- lib/
|   `-- project_name/
|       |-- cli.rb
|       `-- command.rb
`-- spec/
```

For Rails, start with the Rails generator and use Rails directory conventions. Add service objects, form objects, value objects, or app-specific modules only when they simplify real behavior.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Gem | `.gemspec`, `lib/`, `spec/` or `test/` | Keep public API small and documented. |
| CLI | `exe/`, `lib/project_name/cli.rb` | Keep option parsing separate from behavior. |
| Rails app | Rails default layout | Keep controllers/callbacks thin and models cohesive. |
| Background worker | Rails/app job or service layout | Test job behavior and retry/idempotency. |
| Legacy app | Existing layout plus Bundler/RuboCop/tests | Add checks incrementally and avoid large rewrites. |

## Naming And Style

- Use `snake_case` for files, methods, variables, and symbols.
- Use `CamelCase` for classes and modules.
- Use `SCREAMING_SNAKE_CASE` for constants.
- Match file paths to constants: `lib/project_name/customer_importer.rb` defines `ProjectName::CustomerImporter`.
- Use predicate method names ending in `?` and destructive methods ending in `!` only when the non-bang version exists or danger is meaningful.
- Prefer expressive method names over comments explaining unclear behavior.
- Keep methods small, but do not split cohesive logic into ceremony-heavy objects.
- Avoid monkey patches unless isolated, documented, and tested.

## API And Object Design

- Keep public API intentional; Ruby makes accidental public methods easy.
- Use keyword arguments for options with names.
- Prefer plain Ruby objects for domain behavior that does not need Active Record callbacks or framework lifecycle.
- Keep Rails models focused on persistence, validations, and close domain behavior; avoid giant model objects.
- Keep controllers as HTTP coordinators: authorize, validate, call application code, render.
- Avoid global mutable state and class variables for request-specific data.
- Use blocks when they improve resource handling or iteration, not as a substitute for clear objects.
- Prefer explicit dependency injection for clients, clocks, and configuration in testable code.

## Bundler And Dependency Policy

- Use `bundle exec` for project-local tools.
- Commit `Gemfile.lock` for applications and Rails projects.
- Gems should define runtime and development dependencies in the gemspec; lock file policy depends on repository convention.
- Keep Ruby and Rails version constraints explicit.
- Avoid adding broad dependencies for small helpers.
- Run `bundle update <gem>` deliberately rather than updating everything casually.

## Tooling Defaults

Recommended commands:

```bash
bundle install
bundle exec rubocop
bundle exec rspec
bundle exec rake test
bundle exec rake build
bundle audit check
```

Use the commands that match the selected test framework. Rails apps may use:

```bash
bin/rails test
bin/rails test:system
bin/rubocop
```

Prefer app-local binstubs (`bin/rails`, `bin/rubocop`) when the app provides them.

## Testing And TDD

- Put RSpec tests under `spec/`; Minitest tests under `test/`.
- Start with one failing test for a public method, service object, command, controller behavior, or model rule.
- Prefer request/system tests for integrated Rails behavior and unit tests for domain behavior.
- Avoid testing private methods directly unless extracting them would make the design worse.
- Use factories/fixtures conservatively; keep setup visible and meaningful.
- Test validation failures, authorization failures, idempotency, and background job retry behavior where relevant.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Dependencies | `bundle install` | Resolves project gems. |
| Style/lint | `bundle exec rubocop` | Enforces Ruby style and quality rules. |
| Tests | `bundle exec rspec` or `bin/rails test` | Runs behavior/regression tests. |
| Build gem | `bundle exec rake build` | Verifies gem package output. |
| Vulnerabilities | `bundle audit check` | Checks known vulnerable gems. |

For Rails, include database migration/schema checks and app boot checks in CI.

## CI Baseline

```bash
ruby -v
bundle install
bundle exec rubocop
bundle exec rspec
```

For Rails:

```bash
bin/rails db:prepare
bin/rails test
bin/rubocop
```

Run supported Ruby versions in a matrix for gems. Keep database/service dependencies explicit.

## Security And Robustness

- Avoid `eval`, dynamic constant lookup from user input, and unsafe YAML/object deserialization.
- Use parameterized queries or Active Record query APIs.
- Escape output by context and rely on Rails helpers where appropriate.
- Keep secrets in credentials or environment, not committed config.
- Validate uploads and background job inputs.
- Avoid callbacks that hide important side effects.

## Review Hot Spots

- Fat Rails models/controllers and callback-heavy behavior.
- Unpinned Ruby/Rails versions.
- Tests that require full Rails boot for pure domain logic.
- Monkey patches and open classes.
- `rescue StandardError` that swallows failures.
- N+1 queries and unbounded Active Record loads.
- Gem public API changed without versioning thought.
