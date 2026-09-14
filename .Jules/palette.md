## 2026-07-08 - Markdown Table Codeblock Pitfall for Semantic Elements
**Learning:** Wrapping `<abbr>` or markdown links (`[text](url)`) inside backticks within Markdown table cells disables browser hover tooltips and interactive link capabilities by turning them into raw code blocks.
**Action:** Always place raw HTML tags like `<abbr>` and standard markdown links directly inside table cells without backticks so screen readers and interactive pointer events function properly.
