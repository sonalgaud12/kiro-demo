"""In-memory sample data for the Reports API demo.

A real service would read from a database. Keeping it in memory means the
demo runs on any laptop with no setup.
"""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Order:
    order_id: str
    client_id: str
    item: str
    quantity: int
    amount_inr: float
    order_date: date


# API keys map to client IDs. In a real service these would be hashed and stored.
API_KEYS: dict[str, str] = {
    "demo-key-alpha": "alpha-textiles",
    "demo-key-beta": "beta-pumps",
}


ORDERS: list[Order] = [
    Order("ORD-1001", "alpha-textiles", "Cotton fabric (metres)", 500, 62500.0, date(2026, 9, 2)),
    Order("ORD-1002", "alpha-textiles", "Polyester blend (metres)", 300, 33000.0, date(2026, 9, 9)),
    Order("ORD-1003", "alpha-textiles", "Cotton fabric (metres)", 750, 93750.0, date(2026, 9, 23)),
    Order("ORD-2001", "beta-pumps", "Monoblock pump 1HP", 12, 108000.0, date(2026, 9, 5)),
    Order("ORD-2002", "beta-pumps", "Submersible pump 3HP", 4, 86000.0, date(2026, 9, 18)),
]


def orders_for_client(client_id: str) -> list[Order]:
    """Return every order that belongs to one client, oldest first."""
    return sorted(
        (o for o in ORDERS if o.client_id == client_id),
        key=lambda o: o.order_date,
    )
