# Repository Guidelines

## Project Structure & Module Organization
- `src/pycalc_sse/`: Service package. Entry: `pycalc_sse.server:main`.
- `src/pycalc_sse/server.py`: MCP app and CLI.
- Packaging: `pyproject.toml` (src-layout, console script `pycalc-sse`).
- Root docs: `README.md`.

## Build, Test, and Development Commands
- Create env: `python -m venv .venv && source .venv/bin/activate`.
- Install (editable): `pip install -e .`.
- Run server (CLI): `pycalc-sse --host 0.0.0.0 --port 18000`.
- Run module (direct): `python -m pycalc_sse.server`.
- Package (wheel/sdist): `python -m build` (requires `pip install build`).

## Coding Style & Naming Conventions
- Python 3.6+; follow PEP 8 with 4‑space indentation and type hints where reasonable.
- Names: `snake_case` for functions/variables, `UPPER_SNAKE_CASE` for constants (e.g., `_ALLOWED_BINOPS`).
- Keep modules small and focused under `mcp_calc/src/`. Avoid broad imports; prefer explicit exports in `__init__.py` if needed.

## Testing Guidelines
- No tests yet. Prefer `pytest` under `tests/` named `test_*.py`.
- Example: `tests/test_eval.py` for `safe_eval()` (unary ops, floats, errors).
- Run: `pytest -q` (after `pip install pytest`). Target operator whitelist and error branches.

## Commit & Pull Request Guidelines
- Commits: imperative mood, concise scope prefix when helpful (e.g., `server: validate unary ops`).
- Reference issues with `Fixes #123` or `Refs #123`.
- PRs: include a short description, repro/run instructions, and before/after notes for behavior changes. Request review when CI (if present) is green.

## Security & Configuration Tips
- Expression evaluation is intentionally strict via `ast`; do not expand allowed nodes without review.
- Configure host/port via CLI flags or `mcp_calc/config/config.json`. Keep default SSE transport unless you update clients.
- Avoid arbitrary `eval/exec`. Validate inputs at API boundaries and maintain clear error messages.
