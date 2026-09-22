## 2026-07-08 - Table Cell Formatting & Interactive Element Accessibility

**Learning:** Wrapping `<abbr>` or Markdown links (`[text](url)`) inside code backticks (` ``` `) in GitHub Markdown tables renders them as plain code blocks, completely stripping tooltips, hover states, and clickability.
**Action:** Always render HTML `<abbr>` tags and Markdown links directly inside table cells without backtick wrappers to preserve interactive accessibility and browser behaviors.
