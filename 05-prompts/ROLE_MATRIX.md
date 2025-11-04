# Role Comparison Matrix

Abbreviations from 02-dictionary/role_abbreviations.md.

Highlights

- Dormancy: SR controls activation; roles may be set dormant between loops.
- LLM Requirements: Most roles run fine under JSON mode, low temperature; PN surfaces require strict
  safety.

Examples per Role (minimums)

- SR: human.question/response, tu.open/close/checkpoint
- GK: gate.report.submit, gate.decision
- BB: view.export.request/result
- AD/IL: art plan, shotlist
- AuD/AuP: cuelist, audio render notes
- TR: language_pack, register map
- PN: pn.playtest.submit (Cold, player_safe)
