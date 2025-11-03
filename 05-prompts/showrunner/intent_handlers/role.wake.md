# Intent Handler — role.wake (Scaffold)
STATUS: SCAFFOLD
TODO: Flesh out full guidance, examples, and acceptance criteria.


Inputs
- Envelope with `intent = role.wake`, Hot context.

Process
- Activate role session for current TU/loop; share context.

Outputs
- `ack`; optional activation note via `tu.checkpoint`.

