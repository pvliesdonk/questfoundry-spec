# Binding Run Flow

## Sequence

1. **Select Snapshot**
   - Role: Showrunner (SR)
   - Intent: `view.export.request`
   - Context: `hot_cold: "cold"`
   - Safety: `player_safe: true`

2. **Export Result**
   - Role: Lore Writer (LW)
   - Intent: `view.export.result`
   - Context: `snapshot` populated

3. **Submit Playtest**
   - Role: PN
   - Intent: `pn.playtest.submit`
   - Constraints: Cold-only, player-safe

## Envelope Constraints

- `context.hot_cold` MUST be `cold`.
- `safety.player_safe` MUST be `true`.

## Examples

- `view.export.request.json`
- `view.export.result.json`
- `pn.playtest.submit.json`

## References

- `03-schemas/view_log.schema.json`
- `03-schemas/pn_playtest_notes.schema.json`
