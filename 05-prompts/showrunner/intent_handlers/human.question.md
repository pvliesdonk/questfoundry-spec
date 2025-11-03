# Intent Handler — human.question (Scaffold)

Inputs
- Envelope with `intent = human.question`, from any role → SR.

Process
- Present question to human via UI/CLI; await `human.response`.
- Maintain correlation and reply_to linkage.

Outputs
- Forward `human.response` to requesting role; `ack` on receipt.

