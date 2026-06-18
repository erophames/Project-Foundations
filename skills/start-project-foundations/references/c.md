# C Best Practices

Sources:
- SEI CERT C Coding Standard: https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard
- ClangFormat: https://clang.llvm.org/docs/ClangFormat.html
- Clang-Tidy: https://clang.llvm.org/extra/clang-tidy/
- CMake Presets: https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html
- CTest: https://cmake.org/cmake/help/latest/manual/ctest.1.html
- CMake target commands: https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html
- GCC warning options: https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html
- AddressSanitizer: https://clang.llvm.org/docs/AddressSanitizer.html

## Use This Reference

Apply this reference for C libraries, CLIs, embedded components, native extensions, systems daemons, and mixed C/C++ projects where C owns part of the public boundary. C projects need stricter defaults than many languages because undefined behavior, integer conversion, string handling, and ownership bugs are normal failure modes.

Default stance:

- Use target-oriented CMake for portable non-trivial projects.
- Put public headers in `include/project_name/`; keep private headers in `src/`.
- Treat compiler warnings, sanitizers, static analysis, and tests as separate gates.
- Keep APIs explicit about ownership, lifetimes, buffers, and error reporting.
- Use CERT C as the safety baseline, especially at input and memory boundaries.

## Default Structure

Use CMake for portable libraries and CLIs:

```text
project-name/
├── CMakeLists.txt
├── CMakePresets.json
├── include/
│   └── project_name/
│       └── feature.h
├── src/
│   └── feature.c
├── tests/
│   └── feature_test.c
├── .clang-format
└── .clang-tidy
```

Keep public headers in `include/project_name/`. Keep private headers in `src/` or `src/internal/`. Keep generated files out of source directories.

## Project Shape Variants

| Project type | Structure | Notes |
| --- | --- | --- |
| Library | `include/project_name/*.h`, `src/*.c`, `tests/` | Public headers are the contract; keep them self-contained. |
| CLI | `src/main.c`, `src/*.c`, `tests/` | Keep argument parsing and command execution separate from business logic. |
| Embedded | `include/`, `src/`, `platform/`, `tests/host/` | Separate hardware adapters from testable logic. |
| Native extension | language-specific binding folder plus `src/` C core | Test C core independently from binding layer. |
| Mixed C/C++ | C API headers plus C++ internals or separate C target | Use `extern "C"` guards in headers consumed by C++. |

Avoid creating a single `common.c` or `utils.c` early. Split by capability: `ring_buffer.c`, `packet_parser.c`, `file_reader.c`.

## Naming And Style

- Use one clear style enforced by `.clang-format`; do not hand-format by preference.
- Use `snake_case` for functions and variables.
- Use project-prefixed public functions: `project_feature_init`.
- Use `UPPER_SNAKE_CASE` for macros and include guards.
- Prefer `static` for file-local functions and data.
- Keep headers self-contained: each public header should compile when included first.
- Do not hide ownership, allocation, or lifetime in names; document it at API boundaries.

## API Design Rules

- Every public function should make ownership clear: caller-owned, callee-owned, borrowed, or transfer.
- Prefer caller-provided buffers for tight control; return required size when the buffer is too small.
- Return status codes for expected operational failures. Reserve abort/assert for impossible programmer errors.
- Use output parameters consistently and document when they may be `NULL`.
- Keep structs opaque when invariants matter. Expose plain structs only for simple data without invariants.
- Use `size_t` for object sizes and indexes; check conversions when crossing APIs that require `int`, `long`, or fixed-width types.
- Use fixed-width integer types (`uint32_t`, `int64_t`) when binary layout, protocol, or storage width matters.
- Keep public headers minimal. Forward declare where possible and include only what the API needs.
- Do not put executable logic in macros unless the preprocessor is truly required.

## Header Policy

Each public header should:

- Compile when included first in an otherwise empty `.c` file.
- Include its own dependencies.
- Have a project-prefixed include guard or `#pragma once` if the project standard allows it.
- Be usable from C++ if the project expects mixed-language consumers.
- Avoid defining non-`static` objects.
- Avoid including private headers.

Example public header shape:

```c
#ifndef PROJECT_NAME_FEATURE_H
#define PROJECT_NAME_FEATURE_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct project_feature project_feature;

int project_feature_create(project_feature **out_feature);
void project_feature_destroy(project_feature *feature);

#ifdef __cplusplus
}
#endif

#endif
```

## Safety Defaults

- Treat CERT C as the secure-coding baseline, especially input validation, integer conversion, memory management, strings, error handling, and concurrency.
- Compile with high warnings and make CI fail on warnings for new code.
- Prefer bounded APIs and explicit sizes over sentinel assumptions.
- Centralize allocation/free ownership and error cleanup paths.
- Avoid clever macros; use functions unless compile-time behavior is required.

## Memory And Error Handling

- Pair every create/acquire function with a clear destroy/release function.
- Make cleanup paths boring and consistent. A single `goto cleanup;` path is acceptable and often clearer in C.
- Initialize variables at declaration when possible, especially pointers.
- Set freed internal pointers to `NULL` only when it prevents real double-use in the same scope; do not rely on it as a general safety strategy.
- Check allocation failure unless the project has an explicit fatal allocation policy.
- Validate all lengths before allocation, multiplication, or copy.
- Never use `gets`; avoid unbounded string functions; prefer APIs with explicit sizes.
- Treat signed/unsigned conversion warnings as defects.
- Do not ignore return values from allocation, IO, parsing, locking, thread, or security-sensitive APIs.

## Starter CMake Shape

Prefer target-scoped CMake:

```cmake
cmake_minimum_required(VERSION 3.25)
project(project_name C)

add_library(project_name src/feature.c)
target_include_directories(project_name
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
target_compile_features(project_name PUBLIC c_std_17)
target_compile_options(project_name PRIVATE
  $<$<C_COMPILER_ID:Clang,GNU>:-Wall -Wextra -Wpedantic -Wconversion -Wshadow>
  $<$<C_COMPILER_ID:MSVC>:/W4>
)

enable_testing()
add_executable(project_name_tests tests/feature_test.c)
target_link_libraries(project_name_tests PRIVATE project_name)
add_test(NAME project_name_tests COMMAND project_name_tests)
```

Do not put include directories, compile definitions, or warning flags globally unless they truly apply to every target.

## Tooling Defaults

- Formatter: `clang-format`.
- Static analysis: `clang-tidy`, compiler warnings, and sanitizers where supported.
- Build: CMake presets.
- Tests: CTest plus a small C test framework if needed.

Recommended commands:

```bash
cmake --preset dev
cmake --build --preset dev
ctest --preset dev --output-on-failure
clang-format --dry-run --Werror include/**/*.h src/**/*.c tests/**/*.c
clang-tidy -p build/dev src/*.c tests/*.c
```

Adjust globs to the shell and tree. If no compile database exists, generate one with CMake.

## Quality Gates

| Gate | Default command | Purpose |
| --- | --- | --- |
| Configure | `cmake --preset dev` | Generates build files and compile database. |
| Build | `cmake --build --preset dev` | Compiles all targets. |
| Tests | `ctest --preset dev --output-on-failure` | Runs CTest targets. |
| Format | `clang-format --dry-run --Werror ...` | Stable formatting. |
| Static analysis | `clang-tidy -p build/dev ...` | Bug-prone, portability, readability, security checks. |
| Sanitizers | sanitizer preset/build | Runtime memory and UB checks. |

For embedded projects, add a host-test preset and a target-build preset. Do not make hardware availability a requirement for every unit test.

## TDD Guidance

- First test the public header/API shape.
- Keep tests close to behavior: parser input/output, error handling, edge values, allocation failures where practical.
- Write one failing CTest-backed test, run that executable through CTest, then implement.
- Add sanitizer runs for memory-sensitive code: AddressSanitizer, UndefinedBehaviorSanitizer, ThreadSanitizer when relevant.

## Test Design Details

- Keep unit tests as plain C where possible; avoid needing C++ just to test C unless the project already uses a C++ test framework.
- Test public API behavior, invalid inputs, boundary sizes, allocation failure paths where practical, and cleanup idempotence where promised.
- Add compile tests for public headers.
- Use golden files only when the file format is the behavior under test.
- Use fuzz/property-style tests for parsers, protocol decoders, and binary input handling when risk is high.
- Run sanitizers on test binaries, not just application binaries.

## CI Baseline

Run at least two build modes:

```bash
cmake --preset dev
cmake --build --preset dev
ctest --preset dev --output-on-failure
clang-format --dry-run --Werror include/**/*.h src/**/*.c tests/**/*.c
clang-tidy -p build/dev src/*.c tests/*.c
```

For release-sensitive projects, add a release build and one sanitizer build:

```bash
cmake --preset asan
cmake --build --preset asan
ctest --preset asan --output-on-failure
```

## Security Review Hot Spots

- Integer overflow before allocation or copy.
- Buffer length mismatches.
- Null pointer handling in public APIs.
- Lifetime of returned pointers.
- Format strings.
- Path traversal and temporary file handling.
- Thread synchronization and shared state.
- Locale-sensitive parsing.
- Undefined behavior from aliasing, alignment, shifts, object lifetime, or signed overflow.

## Planning Checklist

- Create CMake target per library/executable; avoid global include and compile options.
- Export compile commands for tools.
- Add `.clang-format` and `.clang-tidy`.
- Add first failing test and CTest registration.
- Add warning, sanitizer, and release build verification paths.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Global CMake state everywhere | Use target-scoped compile options, include dirs, and linked libraries. |
| Public headers include private internals | Keep public API small and self-contained. |
| Unclear allocation ownership | Name and document ownership explicitly. |
| Ignoring integer conversion and overflow | Treat conversions as security-sensitive. |
| No sanitizer path | Add sanitizers early; retrofitting is painful. |
