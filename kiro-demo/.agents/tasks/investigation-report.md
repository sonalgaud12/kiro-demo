# Investigation Report: kiro-demo-kit

## Summary

The kiro-demo-kit is a conference talk demo kit for a presentation titled "Future Builders Connect, Coimbatore." It contains two self-contained sub-projects — `demo-api` (a live, on-stage coding demo) and `loomtrack` (a prepared scenario shown as a finished result). Both are Python/FastAPI projects with Kiro steering files that guide the IDE agent's decisions. The kit's central purpose is to demonstrate Kiro IDE's spec-driven development workflow, steering, and agent hooks to a developer audience.

---

## 1. Overall Purpose

`kiro-demo-kit` is a **presentation kit**, not a production codebase. It is structured around a single conference talk (~8-minute live demo, plus a prepared scenario walkthrough). The `DEMO-RUNBOOK.md` is the master script that drives everything: setup the night before, rehearsal, morning checklist, and the live stage sequence with fallback procedures.

The kit demonstrates three Kiro features:
- **Steering files** — per-project `.kiro/steering/` files that constrain how the agent writes code
- **Spec-driven development** — using Kiro's Spec workflow to generate `requirements.md`, `design.md`, and `tasks.md`
- **Agent hooks** — a "run tests on save" hook wired to `python -m pytest -q`

---

## 2. Sub-Projects

### demo-api (Section 8 of the talk — live on stage)

**Purpose:** A small FastAPI backend where "business clients" (textile mills, pump manufacturers) download their order history as CSV. It is deliberately incomplete — it has no rate limiting — so the presenter can add it live on stage using Kiro's spec workflow.

**What it does (before the demo):**
- `GET /health` — liveness check
- `GET /reports/orders` — returns a client's orders as JSON
- `GET /reports/export` — returns a client's orders as a CSV download

**Data:** Entirely in-memory (`app/data.py`). Two hardcoded API keys (`demo-key-alpha` → `alpha-textiles`, `demo-key-beta` → `beta-pumps`) and five sample `Order` records. No database.

**Auth:** `X-API-Key` header resolved by a `current_client` FastAPI dependency in `app/main.py`. Strict data isolation: each key sees only its own orders.

**The live demo task:** Add rate limiting to `/reports/export` — max 5 calls/minute per API key, HTTP 429 + `Retry-After` header on breach, property-based tests with Hypothesis. The expected final output is `200 200 200 429 429 429` when `hit-export.sh` / `hit-export.ps1` fires 6 requests.

**Files:**
| File | Role |
|------|------|
| `app/main.py` | FastAPI app, routes, `current_client` dependency |
| `app/data.py` | In-memory data: `Order` dataclass, `API_KEYS`, `ORDERS`, `orders_for_client()` |
| `tests/test_api.py` | 5 pytest tests covering health, auth rejection, data isolation, CSV shape |
| `hit-export.sh` / `hit-export.ps1` | Scripts to fire 6 requests and print HTTP status codes |
| `requirements.txt` | `fastapi>=0.110`, `uvicorn>=0.29`, `httpx>=0.27`, `pytest>=8.0`, `hypothesis>=6.100` |

---

### loomtrack (Section 9 of the talk — prepared, shown as a result)

**Purpose:** An order tracker for a small powerloom unit (~40 looms) near Coimbatore. The folder is intentionally **empty** of application code. It ships only with Kiro steering files. The night before the talk, the presenter runs Kiro's spec workflow from the prompt in `README.md` to generate the full application, then shows the result on stage.

**Prompt used to generate it:**
> "Build an order tracker for a powerloom unit. Record buyer orders in metres with a delivery date, log daily production, record dispatches, and warn when an order is likely to miss its date."

**Business rules the presenter must verify are in the generated requirements:**
1. Dispatches can never exceed the metres woven so far
2. An order is "At Risk" when projected finish (from recent daily output) is later than delivery date
3. Status only moves forward: Received → In Production → Partly Dispatched → Completed
4. Order quantity can be changed, but never below metres already woven (this is the "gap to add live")

**Files:**
| File | Role |
|------|------|
| `README.md` | Prompt to paste into Kiro Spec, four rules to verify |
| `.kiro/steering/product.md` | Users, problems solved, product rules (Tamil+English labels, decimal metres) |
| `.kiro/steering/structure.md` | Directory layout, module responsibilities, test conventions |
| `.kiro/steering/tech.md` | Stack constraints (SQLite via stdlib, Jinja2, Decimal not float, no cloud) |

---

## 3. Tech Stack, Languages, and Frameworks

| Concern | demo-api | loomtrack |
|---------|----------|-----------|
| Language | Python 3.11+ | Python 3.11+ |
| Web framework | FastAPI | FastAPI |
| Data storage | In-memory (`app/data.py`) | SQLite via stdlib `sqlite3` |
| Templating | None (JSON + CSV responses) | Jinja2 server-rendered HTML |
| Testing | pytest + `TestClient` + Hypothesis | pytest + Hypothesis |
| ASGI server | uvicorn | uvicorn |
| Type hints | Everywhere (required by steering) | Everywhere |
| JavaScript framework | None | None |

---

## 4. Project Conventions

Both sub-projects share the same convention philosophy enforced by their steering files.

### Code style
- **Type hints everywhere** — no untyped functions
- **Small, focused functions** — steering explicitly says "keep functions small"
- **Standard library preferred** — no new third-party dependencies without necessity

### Naming
- Module names are lowercase snake_case (`main.py`, `data.py`, `services.py`)
- Test files mirror the module they test: `app/foo.py` → `tests/test_foo.py`
- Route paths use lowercase kebab-case (`/reports/export`, `/reports/orders`)

### Architecture / structure
- **demo-api:** Cross-cutting logic (e.g., rate limiting) goes in its own `app/` module, never inline in a route function. It is wired in via FastAPI's `Depends()`. Source: `demo-api/.kiro/steering/structure.md`
- **loomtrack:** All business rules live in `app/services.py` (not in routes) so they can be unit-tested directly. Routes are thin. Source: `loomtrack/.kiro/steering/structure.md`

### Testing
- Run command: `python -m pytest -q`
- Endpoint tests use `fastapi.testclient.TestClient`
- Property-based tests use Hypothesis
- **Every new behaviour must have a test** (steering rule in both sub-projects)
- Baseline for demo-api: 5 tests pass before the demo

### API conventions (demo-api)
- Auth: `X-API-Key` request header
- Error responses: JSON `{"detail": "<human-readable message>"}` — this is FastAPI's default `HTTPException` format
- Data isolation: clients must never see each other's data — the top product priority
- The `current_client` dependency in `main.py` is the single auth enforcement point

### LoomTrack-specific conventions
- Quantities in `Decimal` (not `float`) to avoid accumulation drift
- UI labels in both Tamil and English (e.g., "ஆர்டர்கள் / Orders")
- No cloud services — must run on a cheap offline laptop

---

## 5. DEMO-RUNBOOK.md

`DEMO-RUNBOOK.md` is the complete presenter's guide, divided into four parts:

**Part A — Tonight (~60–90 min):** Full setup sequence:
1. Install Kiro IDE and sign in
2. Set up demo-api: create venv, install deps, run 5 baseline tests, `git init`, commit
3. Verify steering shows up in Kiro's panel; test it by asking Kiro "What is this project?"
4. Create the test-on-save agent hook and commit it (this becomes the **baseline commit**)
5. Full rehearsal with screen recording (OBS or Windows Game Bar), save result on `rehearsal-result` branch
6. Prepare LoomTrack: `git init`, run Kiro spec from the README prompt, review/approve requirements+design+tasks, run tasks, run tests, note which property tests were generated, commit, take screenshots
7. Reset demo-api to baseline before bed

**Part B — Morning (15 min):** Pre-talk checklist (laptop charged, Do Not Disturb, Kiro open at baseline, editor zoomed in, two terminals ready, rehearsal recording ready, credits checked)

**Part C — Live demo (8 min):**
1. Show `main.py` and the three steering files, run the server, fire 6 requests → all 200
2. Paste the rate-limiting spec prompt into a new Spec session
3. Review spec: read a WHEN/THEN criterion aloud, edit 5→3 per minute live, ask Kiro to update design+tasks
4. Start first tasks, show the property test, run pytest
5. Restart server, fire 6 requests → `200 200 200 429 429 429`; save a file to trigger the hook

**Part D — Contingency table:**
| Failure | Recovery |
|---------|----------|
| Slow generation | `git stash -u && git checkout rehearsal-result`, show files |
| Wi-Fi / login fails | Phone hotspot or play the screen recording |
| Tests fail | Paste failure once; if not fixed in 30 s, switch to `rehearsal-result` |
| Running out of time | Skip to Step 5 with `rehearsal-result` |

**Reset command:** `git checkout main && git reset --hard && git clean -fd`

---

## 6. Kiro Steering Files

### demo-api — `.kiro/steering/`

| File | Contents |
|------|----------|
| `product.md` | Users (API key clients), data isolation as top priority, expensive CSV export must be protected, error format is JSON `detail` |
| `structure.md` | Directory layout, convention that new cross-cutting logic goes in its own module under `app/` and is plugged in via `Depends`, test file naming mirror convention |
| `tech.md` | Python 3.11+, FastAPI, pytest + TestClient + Hypothesis, no new dependencies, typed functions, every behaviour gets a test, run with `python -m pytest -q` |

### loomtrack — `.kiro/steering/`

| File | Contents |
|------|----------|
| `product.md` | Mill owner + supervisor as non-technical users, buyers place orders by phone/WhatsApp, three problems to solve (visibility, silent delays, dispatch disputes), decimal metres, Tamil+English labels, small first version |
| `structure.md` | Full directory tree (`app/main.py`, `db.py`, `models.py`, `services.py`, `templates/`, `tests/`), business rules in `services.py` not routes, forward-only status progression, test file naming convention |
| `tech.md` | Python 3.11+, FastAPI, SQLite via stdlib `sqlite3`, Jinja2 HTML templates, no JS framework, `Decimal` for metres, offline-only laptop constraint, minimal deps list |

---

## Conclusions

1. **The kit is coherent and well-structured.** The steering files, runbook, and code are tightly aligned. The demo-api steering will guide Kiro to put rate limiting in a separate module with `Depends`, exactly as the presenter wants to point out on stage.

2. **demo-api is deliberately minimal and ready.** The 5 baseline tests pass, the data model is clear, and the architecture is simple enough that an agent can add rate limiting cleanly without touching existing tests.

3. **loomtrack is a shell, by design.** Its value is entirely in the steering files — they're thorough and cover product rules, architecture, tech constraints, and UI conventions. The spec-generation demo depends on these steering files producing a recognisable, opinionated output.

4. **The Hypothesis dependency is pre-loaded** (`hypothesis>=6.100` in `requirements.txt`) even before the demo adds property tests. This is intentional — it avoids a pip install during the live demo.

5. **No gaps or blockers found.** The project is self-contained, runs with no external services, and has clear reset instructions. The only thing that doesn't exist yet on disk is the `.agents/` directory (created for this report).

## Recommendations

- **No code changes needed.** The project is ready for the runbook's Part A setup.
- Consider adding a `.gitignore` to `demo-api/` that excludes `.venv/` and `__pycache__/`, to keep `git status` clean. `loomtrack/` already has a `.gitignore`.
- The runbook says to edit the rate limit from 5→3 per minute live (Step 3). Ensure the Hypothesis property tests generated during rehearsal use a configurable limit, so the edit propagates cleanly to tests.
