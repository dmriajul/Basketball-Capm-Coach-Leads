## 2026-07-08 - Accessible Markdown Micro-UX in Documentation Repositories
**Learning:** In documentation-only repositories, wrapping interactive tags like `<abbr>` or markdown links inside code backticks (` `) breaks their interactive features ( hover tooltips and clickable links). Native GitHub tip admonitions with `<kbd>` elements significantly improve keyboard shortcut discoverability and searchability.
**Action:** Use standard `<abbr title="...">` for team abbreviations and raw `<kbd>` tags in GitHub admonitions without wrapping interactive elements in code backticks.
