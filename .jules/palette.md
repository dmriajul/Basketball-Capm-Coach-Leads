## 2026-07-05 - Semantic Tags in Documentation-Only Repositories
**Learning:** In repositories where the README serves as the primary interface, semantic HTML tags like `<abbr>` for tooltips and `<kbd>` for keyboard shortcuts improve accessibility and scannability, but reviewers may flag them as 'non-technical' or 'low-impact' if they are not explicitly supported by the target platform's renderer (e.g., GitHub's Markdown).
**Action:** Always verify platform-specific Markdown support for semantic HTML tags before implementation to ensure a tangible UX benefit.

## 2026-07-05 - Micro-UX Scope and Boundaries
**Learning:** Reviewers strictly enforce the 'ONE micro-UX improvement' and 'under 50 lines' rules. Bundling diagnostic scripts or data artifacts (like `leads.csv`) with the UX change is seen as scope creep and technical debt.
**Action:** Ensure only the intended UX enhancement and critical project documentation (like journals) are included in the final submission.
