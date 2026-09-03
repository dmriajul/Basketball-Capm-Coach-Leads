## 2026-07-08 - Interactive Element Formatting in Markdown Tables
**Learning:** Wrapping HTML tags (like `<abbr>`) or markdown links inside code backticks inside markdown table cells causes GitHub to render them as raw text rather than interactive elements, completely disabling tooltips and links.
**Action:** Always format `<abbr>`, `mailto:`, and `tel:` tags as raw HTML/Markdown within table cells without backtick wrapping to ensure full keyboard and visual accessibility.
