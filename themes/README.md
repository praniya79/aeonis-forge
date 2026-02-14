# Themes

This folder holds **schema-agnostic** theme definitions for the Seventh River.

Files:
- `seventh-river.toml`
- `seventh-river.json`

They define two layers:

1) **Palette** — named anchors (`river`, `breath`, `core`, etc.)
2) **Roles** — UI intent (`background`, `selectionBg`, `cursorBg`, …)

## How to use

If `openclaw-tui` supports importing themes directly, map its expected keys to the `roles` values.

If it does not (or uses a different schema), translate 1:1:

- `background` → app background
- `text` / `textMuted` → primary/muted text
- `cursorBg` / `cursorFg` → cursor or focus highlight
- `selectionBg` / `selectionFg` → selected row/message
- `accentPrimary` / `accentSecondary` → highlights
- `borderStyle/panelBorder = none` → remove borders

The unchanging anchors are:
- `river  = #4169e1`
- `breath = #e6e6fa`

Everything else may evolve.
