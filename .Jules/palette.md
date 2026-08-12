## 2026-07-08 - Markdown Table Formatting Constraints
**Learning:** Do not wrap HTML `<abbr>` tags or markdown links (`[text](url)`) inside table cells with code backticks in GitHub Markdown tables. Doing so formats them as raw code blocks and completely disables their interactive features (like hovering for tooltips or clicking links), causing code review rejections.
**Action:** Always format `<abbr>` tags and markdown links inside table cells using standard plaintext/HTML elements without code backticks to ensure interactive tooltips and hyperlink capabilities remain fully accessible.
