# Intent Handler — tu.close (Scaffold)
STATUS: SCAFFOLD
TODO: Flesh out full guidance, examples, and acceptance criteria.


Inputs
- Envelope with `intent = tu.close`, Hot context, TU present.

Process
- Finalize session, archive history, emit summary.

Outputs
- `ack` and optional `tu.checkpoint` summary before close.

