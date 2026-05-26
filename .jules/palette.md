# Palette's Journal - Critical UX Learnings

## 2026-05-26 - Documentation as a User Interface (UI)
**Learning:** In documentation-centric repositories, the README.md acts as the primary User Interface. Reducing Time-to-Action (TTA) via semantic HTML (like `<abbr>` and `<kbd>`), clear navigation, and direct "Fast View" links significantly improves the user experience.
**Action:** Use structured layouts, accessible tags, and immediate data previews to enhance README-based UIs.

## 2026-05-26 - Brittle Structural Verification
**Learning:** Hardcoding specific data points (like coach names) in structural verification scripts for documentation-only repositories creates a maintenance burden. Verification should focus on the presence of semantic tags and accessibility patterns rather than specific content.
**Action:** Focus README verification scripts on tag presence (`<abbr>`, `<kbd>`, `mailto:`) rather than ephemeral data.
