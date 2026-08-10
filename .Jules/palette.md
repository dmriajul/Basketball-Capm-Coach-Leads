## 2026-07-08 - Accessible Links and Tooltips in Markdown Tables
**Learning:** Do not wrap HTML <abbr> tags or markdown links inside table cells with code backticks in GitHub Markdown tables, as doing so formats them as raw code blocks and completely disables interactive features like tooltips on hover or link clickability.
**Action:** Always render HTML <abbr> tags and markdown links as plain text elements within Markdown table cells to ensure full interactive and screen-reader accessibility.
