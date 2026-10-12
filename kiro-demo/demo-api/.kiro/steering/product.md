# Product

Reports API is a small backend service. Business clients (textile mills, pump manufacturers) call it to download their own order history.

## Users
- Client systems that call the API with an API key in the `X-API-Key` header.
- Each API key belongs to exactly one client. A client must never see another client's data.

## What matters
- Data isolation between clients is the top priority.
- The CSV export is expensive to generate, so it must be protected from abuse.
- Error responses are JSON with a short, human-readable `detail` message.
