# Tech stack

- Python 3.11+ and FastAPI.
- Tests: pytest. Use `fastapi.testclient.TestClient` for endpoint tests.
- Property-based tests: Hypothesis.
- No database: data lives in memory in `app/data.py`.

## Rules
- Do not add new third-party dependencies unless the task needs one. Prefer the standard library.
- Keep functions small and typed. Use type hints everywhere.
- Every new behaviour gets a test.
- Run tests with: `python -m pytest -q`
