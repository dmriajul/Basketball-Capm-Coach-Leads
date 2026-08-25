## 2026-07-08 - Separated Keyboard Shortcut Hints and Semantic Table Enhancements

**Learning:** Combining modifier and key characters inside a single `<kbd>` tag (e.g., `<kbd>Cmd+F</kbd>`) decreases visual readability and accessible key differentiation. Separating modifier and action keys into individual `<kbd>` tags (e.g., `<kbd>Cmd</kbd> + <kbd>F</kbd>`) significantly improves scannability and accessibility. Additionally, wrapping team abbreviations in `<abbr>` tags (without backticks) provides native hover tooltips without breaking link/tooltip interactivity.

**Action:** Always wrap modifier keys and character shortcuts in separate `<kbd>` tags, and ensure `<abbr>` tags are never enclosed in code backticks within markdown tables.
