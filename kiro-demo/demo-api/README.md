# Reports API (Kiro live demo project)

A tiny FastAPI service used for the live demo. Clients export their orders as CSV from `/reports/export`.

During the demo, Kiro adds rate limiting to that endpoint using a spec.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q              # 5 tests should pass
uvicorn app.main:app --reload
```

Try it:

```bash
curl -H "X-API-Key: demo-key-alpha" http://127.0.0.1:8000/reports/export
```

Sample API keys: `demo-key-alpha`, `demo-key-beta`.
