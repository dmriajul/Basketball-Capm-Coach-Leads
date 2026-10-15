## 2026-07-08 - Accessible Links & Tooltips in Markdown Tables
**Learning:** Wrapping HTML tags like `<abbr>` or markdown links (`[text](url)`) inside code backticks in Markdown table cells disables interactive rendering in GitHub, breaking tooltips and direct navigation.
**Action:** Always format `<abbr>`, `mailto:`, and `tel:` links directly without backticks in Markdown tables to ensure full screen-reader and visual accessibility.
