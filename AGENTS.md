# Repository Guidelines

## Project Structure & Module Organization

This repository is a Copier template for Python packages, not an installable package itself. `copier.yml` defines prompts, defaults, conditional files, and the `template/` subdirectory. `scaffold.sh` generates projects and synchronizes an existing project back into the template. Under `template/`, package code lives in `src/{{ project_slug }}/`, tests in `tests/`, reusable Poe tasks in `bin/poe_tasks.py`, and CI definitions in `.github/workflows/`. Files requiring Copier rendering use the `.jinja` suffix; static files do not.

## Build, Test, and Development Commands

Install template tooling with `pip install copier jinja2-time`. The extension is trusted code, so generation requires Copier's `--trust` flag.

- `./scaffold.sh gen --outdir /tmp/out-copier --project-name plum-tools --version 0.4.1` generates a disposable project.
- From that project, `uv sync` installs development dependencies.
- `uv run poe format` formats `src`, `bin`, and `tests` with Autoflake, isort, Black, and Ruff.
- `uv run poe lint` runs typing, formatting, style, spelling, security, and dead-code checks.
- `uv run poe test` runs pytest with coverage; the default minimum is 50%.
- `./scaffold.sh restore --project-dir /path/to/project` copies project changes back into `template/` and restores Jinja placeholders. Review the resulting diff carefully.

## Coding Style & Naming Conventions

Use four-space indentation for Python and a 120-character line limit. Target Python 3.12 or newer, add type annotations to functions, and keep imports Black/isort compatible. Use `snake_case` for modules, functions, fixtures, and Copier variables. Preserve literal template expressions such as `{{ project_slug }}` and use `.jinja` whenever a file contains Jinja syntax.

## Testing Guidelines

Tests use pytest and belong in `template/tests/` with names matching `test_*.py`; test functions should begin with `test_`. Add tests for template helper behavior and generated package behavior. After template changes, generate a fresh project and run both `uv run poe lint` and `uv run poe test` there. Confirm generated files contain no unintended `{% raw %}` or unresolved placeholders.

## Commit & Pull Request Guidelines

History commonly uses short prefixes such as `ADD:` and `MOD:`. Prefer a descriptive imperative subject, for example `MOD: require explicit restore project directory`, and avoid placeholder messages. Pull requests should explain template and generated-project impact, list validation commands, link relevant issues, and call out changes to Copier prompts, CI, or synchronization exclusions. Include screenshots only when generated documentation has a visual change.
