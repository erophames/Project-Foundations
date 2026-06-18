# Lua Best Practices

Sources:
- Lua 5.4 reference manual: https://www.lua.org/manual/5.4/
- LuaRocks wiki: https://github.com/luarocks/luarocks/wiki/
- StyLua: https://github.com/JohnnyMorganz/StyLua
- Luacheck documentation: https://luacheck.readthedocs.io/en/stable/
- busted documentation: https://lunarmodules.github.io/busted/

## Use This Reference

Apply this reference when Lua owns a script, library, Neovim plugin, game script, embedded extension, OpenResty component, or LuaRocks package. Lua is small and flexible; good projects compensate with clear module boundaries, local variables, tests, and linting.

Default stance:

- Target a specific Lua runtime: Lua 5.1, 5.4, LuaJIT, OpenResty LuaJIT, or host-embedded Lua.
- Use modules that return tables.
- Keep globals out of application code.
- Use StyLua for formatting and Luacheck for static checks.
- Use busted for tests when the project is not constrained by a host runtime.

## Default Structure

For a Lua library:

```text
project-name/
|-- lua/
|   `-- project_name/
|       |-- init.lua
|       `-- feature.lua
|-- spec/
|   `-- feature_spec.lua
|-- rockspec
|-- stylua.toml
|-- .luacheckrc
`-- README.md
```

For a Neovim plugin:

```text
project-name/
|-- lua/
|   `-- project_name/
|       |-- init.lua
|       `-- config.lua
|-- plugin/
|   `-- project_name.lua
|-- doc/
`-- tests/
```

Follow host conventions for games, OpenResty, Redis scripts, or embedded runtimes.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Library | `lua/name/*.lua`, rockspec, specs | Return modules and document public functions. |
| Neovim plugin | `lua/`, `plugin/`, `doc/` | Keep setup thin and behavior in Lua modules. |
| Game script | Engine layout | Isolate engine callbacks from domain logic. |
| OpenResty | nginx/OpenResty layout | Treat request globals as boundary inputs. |
| Embedded Lua | Host-controlled layout | Document runtime version and host APIs. |

## Naming And Style

- Use `snake_case` for variables, functions, and modules unless host conventions differ.
- Use lowercase module paths.
- Use local variables by default: `local value = ...`.
- Use `M` or a named table for module exports, then `return M`.
- Use `_` for intentionally ignored values.
- Avoid globals except for host-required entrypoints.
- Keep metatable magic narrow and documented.
- Prefer explicit table fields over positional tables for public APIs.

## API And Module Design

- Return a table from each module.
- Keep module initialization side effects minimal.
- Validate argument types at public boundaries when misuse is likely.
- Return `nil, err` for recoverable failures when that matches Lua ecosystem expectations.
- Use `error` for programmer errors or unrecoverable states.
- Keep host APIs behind adapters so tests can run outside the host when possible.
- Avoid mutating tables passed by callers unless the function name and docs make mutation clear.
- Avoid relying on global `package.path` changes inside library code.

## Runtime And Dependency Policy

- State supported runtime versions in README and rockspec.
- LuaJIT and Lua 5.4 differ; test the actual runtime users will run.
- Use LuaRocks for distributable dependencies where appropriate.
- Keep dependencies light, especially for embedded and plugin environments.
- Do not assume filesystem, OS, socket, or debug libraries exist in restricted hosts.

## Tooling Defaults

Recommended commands:

```bash
stylua --check lua spec
luacheck lua spec
busted
luarocks test
```

Use host-specific test runners for Neovim, game engines, and OpenResty when behavior depends on host APIs.

## Testing And TDD

- Use busted specs under `spec/` for general Lua projects.
- Start with one failing spec for a public module function, parser, config merger, or host callback adapter.
- Keep host API calls wrapped so pure logic can be tested in ordinary Lua.
- Test nil inputs, missing fields, bad types, and error returns.
- Use temporary directories/files for filesystem behavior.
- For plugins, test setup defaults, user overrides, and lifecycle/reload behavior.

## Quality Gates

| Gate | Command | Purpose |
| --- | --- | --- |
| Format | `stylua --check lua spec` | Enforces style. |
| Static checks | `luacheck lua spec` | Finds globals, unused values, and likely mistakes. |
| Tests | `busted` | Runs behavior specs. |
| Package | `luarocks test` | Runs rockspec-defined checks. |
| Host smoke | Host-specific command | Verifies integration with Neovim/OpenResty/game host. |

## CI Baseline

```bash
lua -v
stylua --check lua spec
luacheck lua spec
busted
```

Run a matrix for Lua versions or LuaJIT when compatibility is promised. Pin tool versions where reproducibility matters.

## Security And Robustness

- Avoid `load`, `loadstring`, and dynamic code execution with untrusted input.
- Validate file paths and host-provided values.
- Avoid leaking state through globals between tests or plugin reloads.
- Treat the debug library as unsafe for normal application logic.
- Keep sandbox limitations documented for embedded hosts.

## Review Hot Spots

- Accidental globals and module-level mutable state.
- Runtime-version assumptions hidden in code.
- Host callbacks with untestable business logic.
- Metatables used where plain tables would be clearer.
- Tests that pass only because previous specs polluted globals.
- Dynamic `require` paths and `package.path` mutation.
