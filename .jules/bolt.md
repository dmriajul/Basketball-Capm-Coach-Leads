# Bolt's Journal - Performance Optimizations

## 2026-03-16 - Optimizing Time-to-Content in Documentation-Centric Repos
**Learning:** In repositories where the README and linked data are the primary product, performance is measured by "Time-to-Content". Bypassing heavy Google Sheets editor interfaces (~320KB) with published web views (~9KB) and providing inline previews significantly improves the user experience.
**Action:** Always provide a lightweight "Quick Preview" and direct, low-overhead links (CSV/pubhtml) for data access.

## 2026-03-16 - Data Integrity vs. Performance
**Learning:** When optimizing for "Time-to-Content" by providing inline previews, there is a risk of data "drift" or manual entry errors (e.g., mismatched coach names and emails). Performance wins are negated if the content is incorrect.
**Action:** Use automated scripts for data cleaning and de-duplication to ensure the "Fast" content is also the "Correct" content.
