## 2026-07-08 - Accessible Markdown Lead Tables & Formatting Constraints

**Learning:** Wrapping interactive HTML tags (like `<abbr>`) or markdown links inside backticks inside GitHub Markdown tables breaks their rendering, causing them to display as raw text and disabling accessibility features (hover tooltips and clickable links).

**Action:** Always place `<abbr>` tags and markdown links directly in table cells without wrapping them in backticks to preserve tooltip hoverability and clickability.
