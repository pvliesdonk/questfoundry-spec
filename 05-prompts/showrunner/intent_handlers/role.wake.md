# Intent Handler — role.wake (Scaffold)

Inputs
- Envelope with `intent = role.wake`, Hot context.

Process
- Activate role session for current TU/loop; share context.

Outputs
- `ack`; optional activation note via `tu.checkpoint`.

