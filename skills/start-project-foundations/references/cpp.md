# C++ Best Practices

Sources:
- C++ Core Guidelines: https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines
- ClangFormat: https://clang.llvm.org/docs/ClangFormat.html
- Clang-Tidy: https://clang.llvm.org/extra/clang-tidy/
- CMake Presets: https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html
- GoogleTest primer: https://google.github.io/googletest/primer.html
- CMake buildsystem manual: https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html
- Sanitizers: https://clang.llvm.org/docs/index.html
- Include What You Use: https://include-what-you-use.org/

## Use This Reference

Apply this reference for C++ libraries, CLIs, services, native modules, game/tooling code, embedded C++, and mixed C/C++ systems. C++ gives powerful abstraction tools; the default stance is to use them to make ownership and invariants explicit without adding framework-heavy architecture.

Default stance:

- Use modern C++ with an explicit standard, normally C++20 or newer unless constrained.
- Use target-oriented CMake and keep build configuration out of source code.
- Prefer RAII, value semantics, and standard library types.
- Keep public headers light and stable.
- Let clang-format, clang-tidy, tests, sanitizers, and builds each do their own job.

## Default Structure

Use target-oriented CMake:

```text
project-name/
├── CMakeLists.txt
├── CMakePresets.json
├── include/
│   └── project_name/
│       └── feature.hpp
├── src/
│   └── feature.cpp
├── tests/
│   └── feature_test.cpp
├── .clang-format
└── .clang-tidy
```

Use `include/` only for public headers. Keep implementation details in `src/` or `src/project_name/internal/`.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Library | `include/project_name/`, `src/`, `tests/` | Public headers define contract; keep internals in source. |
| CLI | `src/main.cpp`, `src/app.cpp`, `tests/` | Keep `main()` tiny; test command behavior through an app layer. |
| Service | `src/domain/`, `src/adapters/`, `src/server/`, `tests/` | Keep network/framework code at boundaries. |
| Game/tool | `src/core/`, `src/platform/`, `assets/`, `tests/` | Separate deterministic core logic from rendering/platform APIs. |
| Embedded | `src/core/`, `src/hal/`, `tests/host/` | Host-test logic without hardware, then add target smoke tests. |

Avoid early `util.hpp` growth. Split by concept: `byte_buffer.hpp`, `asset_cache.hpp`, `tcp_endpoint.hpp`.

## Naming And Style

- Enforce formatting with `.clang-format`; do not debate whitespace manually.
- Follow the C++ Core Guidelines for resource safety, interface design, and modern C++ usage.
- Prefer `snake_case` or local project style consistently; common modern C++ library code often uses `snake_case`, but existing code wins.
- Use `PascalCase` for types only if the project already does; do not mix conventions within one module.
- Use `kConstantName` or `UPPER_SNAKE_CASE` only if established; avoid macro constants when `constexpr` works.
- Keep names proportional to scope; avoid type-encoded names.

## Design Defaults

- Prefer RAII and value semantics.
- Prefer `std::unique_ptr` for unique ownership and references/non-owning pointers for non-ownership.
- Avoid raw `new`/`delete` in application code.
- Use `std::optional`, `std::variant`, and expected-style result types for explicit state.
- Keep headers light; avoid unnecessary transitive includes.
- Mark single-argument constructors `explicit`.
- Make invalid states unrepresentable where practical.

## Ownership And Lifetime

- Use values for simple data and owned objects when copying/moving is cheap or clear.
- Use `std::unique_ptr<T>` for exclusive ownership and `std::shared_ptr<T>` only for genuine shared lifetime.
- Use references or raw pointers for non-owning access. Document nullability when raw pointers are allowed.
- Avoid owning raw pointers in application code.
- Avoid returning references or views to temporaries or invalidated containers.
- Prefer `std::string_view` and `std::span` for non-owning views, but keep lifetime constraints obvious.
- Make resource-owning types non-copyable or define copy behavior explicitly.
- Use RAII wrappers for files, sockets, locks, handles, and temporary state.

## Interface Design

- Keep functions small enough that preconditions and effects are easy to see.
- Use strong types for values with units or domain meaning instead of passing primitive soup.
- Prefer constructors that establish invariants; use factories when construction can fail.
- Mark single-argument constructors `explicit`.
- Use `[[nodiscard]]` for result/status values callers must inspect.
- Use `noexcept` only when the function truly does not throw and the guarantee matters.
- Prefer `enum class` over unscoped enums.
- Prefer algorithms and range-based loops over hand-rolled index loops when clearer.
- Avoid template complexity unless it removes real duplication or enforces useful constraints.

## Error Handling Policy

Choose one primary strategy per boundary:

| Context | Preferred strategy |
| --- | --- |
| Programmer error/invariant violation | `assert`, contract check, or fail-fast according to project policy. |
| Recoverable operational failure | exceptions or expected/result type; be consistent. |
| Low-level/no-exception environments | explicit result/status types. |
| Constructors that can fail | factory returning result/optional or throwing constructor, based on project policy. |
| Destructors | must not throw. |

Do not mix exceptions, integer error codes, boolean failure, and nullable returns for the same layer without a clear adapter boundary.

## Starter CMake Shape

```cmake
cmake_minimum_required(VERSION 3.25)
project(project_name LANGUAGES CXX)

add_library(project_name src/feature.cpp)
target_include_directories(project_name
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
target_compile_features(project_name PUBLIC cxx_std_20)
target_compile_options(project_name PRIVATE
  $<$<CXX_COMPILER_ID:Clang,GNU>:-Wall -Wextra -Wpedantic -Wconversion -Wshadow>
  $<$<CXX_COMPILER_ID:MSVC>:/W4 /permissive->
)

enable_testing()
add_executable(project_name_tests tests/feature_test.cpp)
target_link_libraries(project_name_tests PRIVATE project_name GTest::gtest_main)
add_test(NAME project_name_tests COMMAND project_name_tests)
```

Use FetchContent/package managers only after deciding the dependency strategy. Do not vendor dependencies casually.

## Tooling Defaults

- Build: CMake presets.
- Format: clang-format.
- Static analysis: clang-tidy with `bugprone`, `performance`, `readability`, `modernize`, and selected `cppcoreguidelines` checks.
- Tests: GoogleTest or Catch2; choose the framework already used by the project. GoogleTest is the conservative default for broad team familiarity.

Recommended commands:

```bash
cmake --preset dev
cmake --build --preset dev
ctest --preset dev --output-on-failure
clang-format --dry-run --Werror include/**/*.hpp src/**/*.cpp tests/**/*.cpp
clang-tidy -p build/dev src/*.cpp tests/*.cpp
```

Add sanitizer presets for memory, undefined behavior, and threading when relevant.

## Quality Gates

| Gate | Default command | Purpose |
| --- | --- | --- |
| Configure | `cmake --preset dev` | Generates build and compile database. |
| Build | `cmake --build --preset dev` | Compiles targets. |
| Tests | `ctest --preset dev --output-on-failure` | Runs registered tests. |
| Format | `clang-format --dry-run --Werror ...` | Deterministic formatting. |
| Static analysis | `clang-tidy -p build/dev ...` | Modernization, bug-prone, performance, readability checks. |
| Sanitizers | sanitizer preset/build | Runtime memory, UB, and thread checks. |
| Header hygiene | IWYU or compile public headers | Prevents hidden transitive dependency coupling. |

For libraries, add install/package verification when publishing matters.

## TDD Guidance

- Start with public behavior at the library boundary.
- Use one assertion concept per test; group related cases into suites/sections.
- Prefer deterministic tests with no sleep/time assumptions.
- Use fixtures only when they remove real duplication; avoid shared mutable state.
- Run the smallest test binary first, then full CTest.

## Test Design Details

- Test public behavior and invariants before private implementation details.
- Use typed or parameterized tests for generic algorithms and value types.
- Test move/copy behavior when ownership semantics are important.
- Test exception/result paths explicitly.
- Avoid sleeping in tests; inject clocks or use condition-based waits.
- Use death tests sparingly for intentional fail-fast behavior.
- Keep fixtures small and immutable where possible.
- Add fuzz tests for parsers, binary formats, and untrusted input surfaces.

## Header And Include Policy

- Public headers include what they use and compile standalone.
- Prefer forward declarations only when they reduce coupling without making the header fragile.
- Keep templates and inline functions in headers only when needed.
- Avoid including large framework headers in public API.
- Keep private implementation details out of `include/`.
- Consider a `project_name/detail/` namespace or folder only for implementation that must live in headers.

## CI Baseline

```bash
cmake --preset dev
cmake --build --preset dev
ctest --preset dev --output-on-failure
clang-format --dry-run --Werror include/**/*.hpp src/**/*.cpp tests/**/*.cpp
clang-tidy -p build/dev src/*.cpp tests/*.cpp
```

Add at least one sanitizer job for new systems code:

```bash
cmake --preset asan
cmake --build --preset asan
ctest --preset asan --output-on-failure
```

## Review Hot Spots

- Dangling references, views, iterators, and lambdas capturing by reference.
- Accidental copies of heavy objects.
- Object slicing.
- Shared ownership used to avoid designing lifetime.
- Virtual destructors in base classes.
- Exception safety around partial updates.
- Thread ownership and data races.
- Header bloat and hidden transitive includes.

## Planning Checklist

- Create CMake targets with target-scoped properties.
- Specify the C++ standard explicitly.
- Add format and static-analysis configs.
- Add first failing test with GoogleTest/Catch2.
- Add sanitizer and release build verification.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Header-heavy implementation by default | Keep implementation in `.cpp`; include only what public APIs need. |
| Manual lifetime management | Use RAII and smart ownership types. |
| Global CMake include/options | Use target-scoped CMake. |
| Testing implementation details | Test public behavior and observable contracts. |
| Ignoring move/copy semantics | Decide and declare ownership/copy behavior explicitly. |
