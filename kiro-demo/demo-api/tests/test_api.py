"""Existing tests for the Reports API. All of these pass before the demo starts."""

import csv
import io

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
ALPHA = {"X-API-Key": "demo-key-alpha"}
BETA = {"X-API-Key": "demo-key-beta"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_missing_api_key_is_rejected():
    assert client.get("/reports/export").status_code == 401


def test_invalid_api_key_is_rejected():
    assert client.get("/reports/export", headers={"X-API-Key": "nope"}).status_code == 401


def test_list_orders_only_returns_own_orders():
    orders = client.get("/reports/orders", headers=ALPHA).json()
    assert [o["order_id"] for o in orders] == ["ORD-1001", "ORD-1002", "ORD-1003"]


def test_export_returns_csv_for_client():
    response = client.get("/reports/export", headers=BETA)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    rows = list(csv.reader(io.StringIO(response.text)))
    assert rows[0] == ["order_id", "item", "quantity", "amount_inr", "order_date"]
    assert [r[0] for r in rows[1:]] == ["ORD-2001", "ORD-2002"]
