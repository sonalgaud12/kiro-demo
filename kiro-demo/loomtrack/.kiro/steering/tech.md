# Tech stack

- Python 3.11+ and FastAPI.
- SQLite through the standard library `sqlite3` module. No external database server.
- Simple server-rendered HTML pages (Jinja2 templates) for the owner's screens. No JavaScript framework.
- Tests: pytest. Property-based tests: Hypothesis.

## Constraints
- It must run on a cheap laptop in the mill office with no cloud services and no monthly bill.
- Use `Decimal` (not float) for metres, so totals never drift.
- Keep dependencies minimal: fastapi, uvicorn, jinja2, pytest, hypothesis, httpx.
- Run tests with: `python -m pytest -q`
