## 2026-07-08 - Accessibility in GitHub Markdown Tables
**Learning:** Wrapping HTML `<abbr>` tags or Markdown links in backticks inside table cells completely disables interactive features like tooltips on hover and clickability, which fails accessibility reviews.
**Action:** Ensure `<abbr>` tags and Markdown links are left as raw text/HTML inside table cells without code block backticks.
