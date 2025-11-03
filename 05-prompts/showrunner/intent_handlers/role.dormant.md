# Intent Handler — role.dormant (Scaffold)

Inputs
- Envelope with `intent = role.dormant`, Hot context.

Process
- Park role session; persist outstanding notes and deferrals.

Outputs
- `ack`; update dormancy registry.

