# Project structure

```
app/
  main.py      FastAPI app, routes and dependencies
  data.py      In-memory data: API keys and orders
tests/
  test_api.py  Endpoint tests
```

## Conventions
- New cross-cutting logic (for example rate limiting) goes in its own module under `app/`, not inside a route function.
- Plug it into routes with a FastAPI dependency (`Depends`).
- Test files mirror module names: `app/foo.py` is tested by `tests/test_foo.py`.
