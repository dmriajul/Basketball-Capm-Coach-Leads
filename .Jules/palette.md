## 2026-07-08 - Accessible Micro-UX for Roster Tables
**Learning:** In documentation-only repositories, tables serving as directories are highly optimized by adding native browser shortcuts, explicit `<abbr>` tags for abbreviations, and standard communication links (mailto, tel) with raw values inside labels for better accessibility and Time-to-Action.
**Action:** Always avoid wrapping interactive elements like `<abbr>` or markdown links inside code backticks in table cells to keep tooltips and links clickable, and leverage separate `<kbd>` elements inside TIP admonitions.
