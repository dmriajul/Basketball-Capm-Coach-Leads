## 2026-06-01 - Document-as-UI Performance via pubhtml
**Learning:** In documentation-only repositories where a README serves as the primary interface, providing a direct 'Fast View' link to a Google Sheets 'pubhtml' export (~9KB) reduces the initial data access payload by ~97% compared to the full spreadsheet editor UI (~300KB+), significantly improving Time-to-Content (TTC).
**Action:** Prioritize lightweight 'pubhtml' exports over heavy editor links for data previews in README-based interfaces.
