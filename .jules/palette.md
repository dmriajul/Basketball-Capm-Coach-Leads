## 2026-03-25 - [Accessibility & Navigation]
**Learning:** Using `<abbr>` tags for acronyms improves context for screen readers and provides helpful tooltips on hover. Standard Markdown anchor generation can be inconsistent across platforms; using an explicit `<a name="top"></a>` tag ensures a reliable "Back to Top" destination.
**Action:** Always prefer explicit HTML anchors for critical internal navigation in READMEs to bypass platform-specific header slugification issues.
