"""Reports API: a small service that lets clients export their orders as CSV.

Run it:   uvicorn app.main:app --reload
Try it:   curl -H "X-API-Key: demo-key-alpha" http://127.0.0.1:8000/reports/export
"""

import csv
import io

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import PlainTextResponse

from app.data import API_KEYS, orders_for_client

app = FastAPI(title="Reports API", version="0.1.0")


def current_client(x_api_key: str | None = Header(default=None)) -> str:
    """Resolve the calling client from the X-API-Key header."""
    if x_api_key is None or x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    return API_KEYS[x_api_key]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/reports/orders")
def list_orders(client_id: str = Depends(current_client)) -> list[dict]:
    """Return the client's orders as JSON."""
    return [
        {
            "order_id": o.order_id,
            "item": o.item,
            "quantity": o.quantity,
            "amount_inr": o.amount_inr,
            "order_date": o.order_date.isoformat(),
        }
        for o in orders_for_client(client_id)
    ]


@app.get("/reports/export", response_class=PlainTextResponse)
def export_orders(client_id: str = Depends(current_client)) -> PlainTextResponse:
    """Export the client's orders as a CSV file.

    This endpoint is expensive in a real system (it scans the whole order
    history), which is why it is the one we want to protect with rate limiting.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["order_id", "item", "quantity", "amount_inr", "order_date"])
    for o in orders_for_client(client_id):
        writer.writerow([o.order_id, o.item, o.quantity, f"{o.amount_inr:.2f}", o.order_date.isoformat()])

    return PlainTextResponse(
        buffer.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{client_id}-orders.csv"'},
    )
