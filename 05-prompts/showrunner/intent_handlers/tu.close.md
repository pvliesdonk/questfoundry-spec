# Intent Handler — tu.close (Scaffold)

Inputs
- Envelope with `intent = tu.close`, Hot context, TU present.

Process
- Finalize session, archive history, emit summary.

Outputs
- `ack` and optional `tu.checkpoint` summary before close.

