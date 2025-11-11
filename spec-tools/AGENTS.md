# Agent Guidelines (spec-tools)

> **Parent Guidelines:** See [`../AGENTS.md`](../AGENTS.md) for:
> - Universal assistant rules (clarity, conciseness, expert opinions)
> - QuestFoundry specification context (Layers 0-5, architectural principles)
> - Commit conventions and branch workflow
> - Markdown formatting guidelines

This file extends the parent with **Python-specific guidelines** for the `spec-tools/` validation
and build tools.

---

## Project Context (spec-tools)

The `spec-tools/` directory contains Python tools for validating and building QuestFoundry
specification artifacts:

### Repository Structure

```
spec-tools/
├── src/
│   └── qfspec/          # Main Python package
│       ├── validators/  # Schema and artifact validators
│       ├── builders/    # Kit builders (upload_kits)
│       └── cli.py       # CLI entry points
├── tests/               # Pytest test suite
├── scripts/             # Shell scripts (build_upload_kits.sh, etc.)
├── pyproject.toml       # Dependencies and uv/ruff configuration
├── README.md            # Tool documentation
└── AGENTS.md            # <-- This file (Python coding standards)
```

### Key Tools

- **`qfspec-validate-schemas`** — Validate all JSON schemas against JSON Schema Draft 2020-12
  meta-schema
- **`qfspec-validate-artifact`** — Validate artifact instance against its schema
- **`qfspec-build-kits`** — Build upload kits (minimal, optional, full) for Layer 5 prompts

### Related Specification Files

- **Schema definitions**: `../03-schemas/*.schema.json`
- **Layer 2 templates**: `../02-dictionary/artifacts/*.md` (source for schema generation)
- **Layer 5 prompts**: `../05-prompts/` (built into upload kits)

---

## Python Coding Guidelines

These rules apply to all Python code (`*.py`) in `spec-tools/`.

### Python Version

Write for Python 3.11-3.13. Do NOT write code to support earlier versions.
Always use modern Python practices, including full type annotations and generics.

### Project Setup and Developer Workflows

- **ALWAYS use uv** for running all code and managing dependencies.
- Never use direct `pip` or `python` commands.
- Use modern `uv` commands: `uv sync`, `uv run ...`, `uv add`.

- Use the following commands to ensure quality:

  ```shell
  # Install/sync all dependencies:
  uv sync
  
  # Run linting (ruff) and type checking (mypy):
  uv run ruff check .
  uv run mypy
  
  # Run tests:
  uv run pytest
  
  # Auto-format code
  uv run ruff format .
  ```

- To see test output for individual tests, run:
  `uv run pytest -s tests/some/file.py`

- You must verify there are zero linter warnings/errors or test failures before
  considering any task complete.

### General Development Practices

- Be sure to resolve pyright/mypy linter errors as you develop.
- If type checker errors are hard to resolve, you may add a comment `# pyright: ignore`
  to disable warnings or errors *only* if you know they are not a real problem
  and are difficult to fix.
- DO NOT globally disable lint or type checker rules without confirmation.
- Never change an existing comment, pydoc, or a log statement, unless it is directly
  related to the fix or the user has asked for a cleanup.
  Do not drop existing comments when editing code!

### Coding Conventions and Imports

- Always use full, absolute imports: `from toplevel_pkg.module1.module2 import ...`
- DO NOT use relative imports: `from .module1.module2 import ...`
- Be sure to import types from `collections.abc` or `typing_extensions` where appropriate.
  (e.g., `from collections.abc import Callable, Coroutine`)
- Use `typing_extensions` for `@override` (to support Python 3.11).
- Add `from __future__ import annotations` on files with types whenever applicable.
- Use `pathlib.Path` instead of strings for paths.
  Use `Path(filename).read_text()` instead of `with open(...)`.

### Use Modern Python Practices

- ALWAYS use `@override` decorators (from `typing_extensions`) when overriding methods.

### Testing

- Place tests in the `tests/` directory.
- For simple tests, prefer inline functions in the original code file below a `## Tests`
  comment. Inline tests should NOT import pytest.
- DO NOT write one-off test code in throwaway files.
- DO NOT put `if __name__ == "__main__":` for quick testing.
- Just write `assert x == 5`. Do NOT write `assert x == 5, "x should be 5"`.
- DO NOT write trivial tests (e.g., asserting a constant's value or simple Pydantic instantiation).
- NEVER write `assert False`. Use `raise AssertionError("Some explanation")` instead.
- DO NOT use pytest fixtures (like parameterization) unless absolutely necessary.

### Types and Type Annotations

- Use modern union syntax: `str | None` (NOT `Optional[str]`).
- Use `dict[str]` (NOT `Dict[str]`), `list[str]` (NOT `List[str]`), etc.
- Never use/import `Optional` for new code.

### Guidelines for Literal Strings

- For multi-line strings, ALWAYS use `textwrap.dedent` to make them readable.
  Example:

  ```python
  from textwrap import dedent
  
  markdown_content = dedent("""
      # Title 1
      Some text.
      """).strip()
  ```

### Guidelines for Comments

- Comments should be EXPLANATORY: Explain *WHY*, not *WHAT*.
- Comments should be CONCISE.
- DO NOT use comments to state obvious things. (e.g., `if self.failed == 0: # All successful`).

### Guidelines for Docstrings

- Use concise pydoc strings with triple quotes on their own lines.
- Use `backticks` around variable names and inline code.
- Docstrings should explain rationale or pitfalls, not obvious details from types/names.
- Avoid obvious or repetitive docstrings.
- Do NOT list args and return values if they're obvious from the signature.
- Public/exported functions/methods SHOULD have concise docstrings.
- Internal/local functions/methods DO NOT need docstrings unless their purpose is not obvious.

### General Clean Coding Practices

- Avoid writing trivial wrapper or delegation functions.
- If a function does not use a parameter, use `# pyright: ignore[reportUnusedParameter]` to suppress the linter warning.

### Guidelines for Backward Compatibility

- If a change to an API or library will break backward compatibility, MENTION THIS.
- DO NOT implement backward-compatibility code unless explicitly confirmed.
