# JavaScript Best Practices

Sources:
- Google JavaScript Style Guide: https://google.github.io/styleguide/jsguide.html
- ESLint configuration docs: https://eslint.org/docs/latest/use/configure/
- Prettier options: https://prettier.io/docs/options
- npm `package.json`: https://docs.npmjs.com/cli/v10/configuring-npm/package-json
- Node.js test runner: https://nodejs.org/api/test.html
- Node.js ECMAScript modules: https://nodejs.org/api/esm.html
- Node.js packages: https://nodejs.org/api/packages.html
- npm package lock files: https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json

## Use This Reference

Apply this reference to plain JavaScript projects: Node libraries, CLIs, browser scripts, small packages, test utilities, and framework apps whose core logic is JavaScript. If the user chooses TypeScript, use this as the JavaScript runtime baseline but add TypeScript-specific compiler and declaration guidance from the selected framework or project standard.

Default stance:

- Prefer ESM for new Node projects unless a target runtime or package ecosystem requires CommonJS.
- Use named exports for internal project modules unless the framework strongly expects default exports.
- Keep package scripts as the local contract for test, lint, format, and build.
- Do not create framework-specific folders before the framework is selected.
- Keep runtime code in `src/` and tests in `test/` for package/library/CLI work.

## Default Structure

Use a small package structure before introducing framework folders:

```text
project-name/
|-- package.json
|-- package-lock.json
|-- eslint.config.js
|-- src/
|   `-- index.js
`-- test/
    `-- index.test.js
```

For browser or full-stack apps, follow the framework's standard layout after the framework is selected. Keep domain logic separate from route/component glue.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Node library | `src/`, `test/`, `package.json`, `eslint.config.js` | Export a small public surface from `src/index.js`. |
| CLI | `src/cli.js`, `src/index.js`, `bin` entry in `package.json` | Keep CLI parsing thin; test command behavior without shelling out for every case. |
| Browser widget | `src/`, `test/`, optional `public/` | Keep DOM integration thin and pure logic testable. |
| Full-stack/framework | framework default plus extracted `src/lib/` or equivalent | Do not fight framework conventions, but keep business logic out of route glue. |
| Package with build | `src/`, `dist/` ignored or generated, `exports` map | Publish only intended files; test source and package output when packaging matters. |

Avoid generic `helpers.js` or `utils.js` as the first shared file. Prefer `parse-arguments.js`, `format-currency.js`, `user-repository.js`, or similar responsibility names.

## Naming And Style

- Use `lowerCamelCase` for variables, functions, methods, and properties.
- Use `UpperCamelCase` for classes and components.
- Use `UPPER_SNAKE_CASE` only for true constants.
- Use consistent file naming. For new Node packages, prefer `kebab-case.js` for files unless a framework expects another style.
- Prefer ESM for new Node projects unless the target runtime or ecosystem requires CommonJS.
- Avoid implicit globals and mutation-heavy module state.
- Use JSDoc or TypeScript when public APIs need durable contracts. Do not create a TypeScript project unless the user chooses it or the ecosystem expects it.

## Module And API Design

- Keep top-level modules side-effect-light. Importing a module should not start a server, parse CLI args, connect to a database, or read secrets.
- Use small exported functions and classes with explicit input/output behavior.
- Keep `index.js` as an export boundary, not a dumping ground.
- Prefer `AbortSignal` and timeouts for async operations that can hang.
- Avoid mutation-heavy exported objects. Export functions or immutable values.
- Pass filesystem roots, clocks, random generators, and clients as parameters where tests need control.
- Use `Error` subclasses sparingly; add them when callers can branch on type.
- Keep environment variable access in one config module.

## Starter `package.json`

Use this as a baseline for Node packages:

```json
{
  "name": "project-name",
  "version": "0.1.0",
  "type": "module",
  "private": true,
  "engines": {
    "node": ">=22"
  },
  "scripts": {
    "test": "node --test",
    "lint": "eslint .",
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  },
  "dependencies": {},
  "devDependencies": {
    "@eslint/js": "latest",
    "eslint": "latest",
    "prettier": "latest"
  }
}
```

For publishable packages, remove `"private": true`, define `license`, `files`, `exports`, and package entrypoints deliberately. Do not publish broad repo contents by accident.

## Starter `eslint.config.js`

```javascript
import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    files: ['src/**/*.js', 'test/**/*.js'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    rules: {
      'no-console': 'off',
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
];
```

For browser projects, add browser globals intentionally. For Node projects, add Node globals through the chosen ESLint globals package or project config.

## Dependency And Runtime Policy

- Commit `package-lock.json` for applications, CLIs, and services.
- For libraries, still keep a lockfile for development reproducibility unless the publishing policy says otherwise.
- Pin runtime through `engines`, `.nvmrc`, `.node-version`, or deployment config.
- Avoid package churn for trivial utilities. Modern Node includes many capabilities that used to require dependencies.
- Prefer mature dependencies with clear maintenance, small transitive trees, and active security response.
- Keep dev dependencies separate from runtime dependencies.

## Tooling Defaults

- Package manager: npm with committed lockfile unless the user chooses pnpm or Yarn.
- Formatter: Prettier.
- Linter: ESLint flat config.
- Tests: Node's built-in test runner for simple libraries/CLIs; Vitest/Jest when the app/framework already benefits from them.
- Runtime version: pin with `.nvmrc`, `.node-version`, or `engines` when deployment depends on it.

Recommended commands:

```bash
npm test
npm run lint
npm run format:check
npm run build
```

Only include `build` when the project actually has a build step.

## Quality Gates

| Gate | Default command | Purpose |
| --- | --- | --- |
| Tests | `npm test` | Behavior and regression coverage. |
| Lint | `npm run lint` | Static correctness, unused values, unsafe patterns. |
| Format check | `npm run format:check` | Prettier consistency. |
| Build | `npm run build` | Bundled/transpiled output when applicable. |
| Package smoke | `npm pack --dry-run` | Confirm publish contents for packages. |

For browser apps, add a minimal DOM/render smoke test and a production build check. For CLIs, test exit code, stdout, stderr, and invalid arguments.

## TDD Guidance

- Put tests under `test/` or next to files only if the framework standard says so.
- Test exported behavior rather than private module details.
- For CLI apps, test argument parsing and command execution without spawning a process for every case.
- For browser code, test pure logic separately from DOM rendering.
- Use fake timers and dependency injection for time, random, filesystem, and network boundaries.

## Test Design Details

- Use the built-in Node test runner for small libraries and CLIs to avoid unnecessary dependency weight.
- Use Vitest/Jest when the framework ecosystem expects richer mocking, browser-like environments, or snapshot support.
- Keep tests deterministic: no real network by default, no current-clock assumptions, no order dependence.
- Use `node:assert/strict` with the Node runner.
- Test ESM import/export contracts for libraries.
- For async code, assert both success and rejection paths.
- For modules that consume environment variables, reset environment state in `afterEach`.

## Security And Robustness Defaults

- Never pass unsanitized user input to `eval`, `Function`, dynamic import paths, shell commands, or HTML injection APIs.
- Use `child_process.spawn`/`execFile` with argument arrays for subprocesses.
- Validate JSON and external inputs before using nested fields.
- Use `URL` and `URLSearchParams` instead of string concatenation for URLs.
- Put network timeouts and aborts on external calls.
- Keep secrets out of logs, thrown error messages, snapshots, and test fixtures.
- For browser code, treat `innerHTML` and URL construction as security-sensitive.

## CI Baseline

Run checks from package scripts:

```bash
npm ci
npm run format:check
npm run lint
npm test
npm run build
```

Use `npm ci` in CI because it installs from the lockfile. Skip `npm run build` only when the package has no build step.

## Planning Checklist

- Choose runtime target: Node, browser, or framework.
- Create `package.json` scripts for test, lint, and format check.
- Add ESLint and Prettier config.
- Add first failing test with the chosen runner.
- Add lockfile and runtime version pin when reproducibility matters.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Starting with framework folders before choosing a framework | Begin with `src/` and `test/`, then adopt framework defaults. |
| Mixing ESM and CommonJS casually | Pick one module system and configure it explicitly. |
| No lockfile | Commit the package manager lockfile for applications and CLIs. |
| Lint and format rules fighting | Let Prettier own formatting and ESLint own correctness. |
| Logic trapped inside routes/components | Extract pure functions and services for testing. |
