# Palette's Journal - UX & Accessibility Learnings

## 2026-07-08 - Table Cell Code Backticks Disable Interactive HTML Elements
**Learning:** Wrapping HTML tags (like `<abbr>` or `<a>`) in markdown code backticks inside table cells causes GitHub to render them as raw text rather than interactive elements, disabling tooltips and links.
**Action:** Always place `<abbr>` and `<a>` tags directly in table cell text without wrapping them in backticks.
