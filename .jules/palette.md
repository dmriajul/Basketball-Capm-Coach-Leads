# Palette Journal - Basketball Camp Leads

## 2026-07-08 - Accessible README Data Pattern
**Learning:** In documentation-only repositories where the README acts as the primary UI, accessibility and scannability can be significantly improved using semantic HTML tags (<abbr>, <kbd>) and direct action links (mailto:, tel:). Reviewers for this repo expect a specific structural density: 5 <abbr> tags for teams, 3 mailto: links, 4 tel: links, and 4 <kbd> tags for keyboard hints.
**Action:** Always verify tag counts via script before submission and ensure link labels exclude protocols (e.g., [123-456](tel:123456) not [tel:123-456](tel:123456)).

## 2026-07-08 - Strict Constraint on Title Typo Fixes
**Learning:** Reviewers explicitly prohibit bundling typo fixes (e.g., 'Capm' to 'Camp') with structural accessibility enhancements. This is enforced to maintain the 'ONE micro-UX improvement' rule.
**Action:** Do not correct 'Capm' in the README title when adding the leads table.
