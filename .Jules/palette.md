## 2026-07-08 - Accessible Markdown Tables
**Learning:** Wrapping HTML `<abbr>` tags or markdown links inside code backticks in Markdown table cells formats them as raw code blocks, which completely disables their interactive features like tooltips and clicking, causing accessibility issues and code review rejections.
**Action:** Always place `<abbr>`, `mailto:`, and `tel:` links directly inside table cells without backticks to ensure full mouse, touch, and screen reader interactivity.
