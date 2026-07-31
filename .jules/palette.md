## 2026-07-08 - Basketball Camp Leads Table Accessibility
**Learning:** Do not wrap HTML `<abbr>` tags or markdown links (`[text](url)`) inside table cells with code backticks in GitHub Markdown tables. Doing so formats them as raw code blocks and completely disables their interactive features (like hovering for tooltips or clicking links), causing code review rejections.
**Action:** When adding accessible components to markdown tables, keep them un-backticked so they render as interactive HTML and markdown elements.
