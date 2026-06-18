# TypeScript Best Practices

Sources:
- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/intro.html
- TSConfig reference: https://www.typescriptlang.org/tsconfig/
- typescript-eslint getting started: https://typescript-eslint.io/getting-started/
- Vitest guide: https://vitest.dev/guide/

## Use This Reference

Apply this reference when TypeScript is the primary language for a package, CLI, Node service, browser app, full-stack app, library, monorepo package, or migration from JavaScript. TypeScript projects should use the compiler as a design tool, not just a transpiler. Start strict, keep runtime boundaries explicit, and avoid turning off type checks to preserve JavaScript habits.

Default stance:

- Use `tsconfig.json` with `strict: true`.
- Use ESM unless the runtime or package ecosystem requires CommonJS.
- Keep source in `src/`, tests in `test/` or colocated `*.test.ts`.
- Use `tsc --noEmit` for type checking even when bundlers transpile code.
- Use typescript-eslint for linting and Vitest for conservative new-project tests.
- Treat generated code and declaration files as separate from hand-written source.

## Default Structure

For a library or Node package:

```text
project-name/
|-- package.json
|-- tsconfig.json
|-- src/
|   |-- index.ts
|   `-- feature.ts
|-- test/
|   `-- feature.test.ts
`-- README.md
```

For a CLI:

```text
project-name/
|-- package.json
|-- tsconfig.json
|-- src/
|   |-- cli.ts
|   |-- main.ts
|   `-- commands/
`-- test/
    |-- cli.test.ts
    `-- fixtures/
```

For frontend or full-stack projects, follow the framework's generated layout but keep domain logic in importable modules and test it outside UI rendering where possible.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Library | `src/index.ts`, `src/*.ts`, `test/` | Export intentionally; emit declarations for published packages. |
| CLI | `src/cli.ts`, `src/main.ts`, `test/cli.test.ts` | Keep process exit and console IO at the edge. |
| Node service | `src/app`, `src/config`, `src/adapters`, `test/` | Keep framework handlers thin and validate inputs at boundaries. |
| Browser app | Framework layout plus typed domain modules | Separate API clients, state, and pure domain logic from components. |
| Monorepo | `packages/*`, shared base tsconfig | Use project references only when build boundaries justify them. |
| JS migration | `allowJs` temporarily, incremental strictness | Set a migration target and remove compatibility flags over time. |

Avoid `types.ts`, `utils.ts`, and `helpers.ts` as first modules. Prefer names like `invoice.ts`, `parse_config.ts`, `http_client.ts`, or `user_permissions.ts`.

## Naming And Style

- Use `camelCase` for variables, functions, methods, and properties.
- Use `PascalCase` for classes, interfaces, type aliases, enums, and React components.
- Use `UPPER_SNAKE_CASE` for true constants.
- Prefer descriptive type names: `UserRepository`, `InvoiceLine`, `ParseResult`.
- Avoid Hungarian-style prefixes such as `IUser` for interfaces.
- Prefer `type` for unions, mapped types, and simple object aliases; use `interface` when extension/merging is useful.
- Use named exports for most library code; reserve default exports for framework conventions or single obvious exports.
- Keep file names consistent with the codebase. `kebab-case.ts` and `camelCase.ts` both appear in real projects; do not mix without reason.
- Keep public exports documented when the package is consumed outside the repo.

## Type Design

- Start with `strict: true`, `noUncheckedIndexedAccess`, and `exactOptionalPropertyTypes` when the project can tolerate the stricter ergonomics.
- Use `unknown` at untrusted boundaries, then validate or narrow.
- Avoid `any`. If unavoidable, isolate it in adapter code with a comment explaining the boundary.
- Prefer discriminated unions for closed states and result variants.
- Avoid `enum` for public package APIs unless runtime enum objects are required; string literal unions often interoperate better.
- Use branded or opaque types for IDs and units when accidental mixing is risky.
- Keep generic types simple. If a type needs heavy conditional machinery, ask whether the API is too clever.
- Do not rely on TypeScript for runtime validation. Use explicit parsers/validators at JSON, environment, CLI, form, and network boundaries.

## Build And Dependency Policy

- Pick one package manager per repo and commit its lock file.
- Use `tsc --noEmit` for checking and a bundler/transpiler only when packaging or runtime needs it.
- For published packages, define `exports`, `types`, and supported module formats deliberately.
- Keep Node version in `engines`, `.nvmrc`, `.node-version`, or the repo's chosen version manager.
- Keep path aliases minimal; they can hide package boundaries and complicate published output.
- For monorepos, use workspace-native tooling first and add build orchestration only when package count or dependency graph requires it.

Starter `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "declaration": true,
    "sourceMap": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src", "test"]
}
```

## Tooling Defaults

Recommended commands:

```bash
npm run typecheck
npm run lint
npm run test
npm run build
npm audit
```

Typical scripts:

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "lint": "eslint .",
    "test": "vitest run",
    "build": "tsc -p tsconfig.json"
  }
}
```

Use Prettier or Biome for formatting if the repo already standardizes on it. Do not make ESLint handle formatting unless the project already does.

## Testing And TDD

- Put tests in `test/` for public behavior or colocate `*.test.ts` beside source for small packages.
- Start with one behavior at the public boundary: parser, service method, command runner, reducer, hook, or API client.
- Use Vitest for fast unit tests in new standalone TypeScript projects.
- Use framework-native test tools for UI rendering, routing, and browser behavior.
- Use fake timers, fake clocks, and dependency injection for time and randomness.
- Test runtime validation failures separately from compile-time types.
- Use `expectTypeOf` or type-level tests only for library type contracts; do not let them replace runtime tests.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Type check | `npm run typecheck` | Verifies TypeScript contracts. |
| Lint | `npm run lint` | Enforces code-quality and unsafe-type rules. |
| Tests | `npm run test` | Runs behavior/regression tests. |
| Build | `npm run build` | Confirms emitted output or bundled app. |
| Audit | `npm audit` or ecosystem equivalent | Checks known dependency advisories. |

For package publishing, add tests for generated declarations, package exports, and both ESM/CJS paths if both are supported.

## CI Baseline

```bash
node --version
npm ci
npm run typecheck
npm run lint
npm run test
npm run build
```

Use the repo's package manager equivalent for `npm ci`. Cache package-manager and build caches according to CI platform, but do not cache `node_modules` unless the package manager recommends it.

## Review Hot Spots

- `any`, unsafe casts, non-null assertions, and disabled lint rules.
- Runtime JSON used as trusted typed data.
- Public APIs inferred accidentally from implementation types.
- `ts-ignore` without an issue link or narrow explanation.
- Overly broad path aliases and circular imports.
- Tests that mock the unit under test instead of exercising behavior.
- Build output not matching `exports` and `types` in `package.json`.
