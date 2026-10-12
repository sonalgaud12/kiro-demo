# Project structure

```
loomtrack/
  app/
    main.py        FastAPI app and routes
    db.py          SQLite connection and schema
    models.py      Order, ProductionLog, Dispatch
    services.py    Business rules (status changes, dispatch checks, delay warning)
    templates/     Jinja2 HTML pages
  tests/
```

## Conventions
- All business rules live in `app/services.py`, not in route functions, so they can be tested directly.
- Order status only moves forward: Received, In Production, Partly Dispatched, Completed.
- Test files mirror module names: `app/services.py` is tested by `tests/test_services.py`.
