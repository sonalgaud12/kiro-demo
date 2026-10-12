# LoomTrack (Scenario 1 starter)

This folder is intentionally empty except for Kiro steering files in `.kiro/steering/`.
Kiro builds the app from a spec. Murugan, the mill owner, is a made-up character for the talk.

## Prompt to paste into a new Spec session

> Build an order tracker for a powerloom unit. Record buyer orders in metres with a delivery date, log daily production, record dispatches, and warn when an order is likely to miss its date.

## What to check in the generated requirements

The talk refers to these rules. If Kiro did not include one, add it yourself before approving:

1. Dispatches can never exceed the metres woven so far.
2. An order is marked At Risk when the projected finish date (from recent daily output) is later than the delivery date.
3. Status only moves forward: Received, In Production, Partly Dispatched, Completed.
4. The gap to add live: an order's quantity can be changed, but never to less than the metres already woven.
