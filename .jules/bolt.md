## 2026-05-28 - Performance Strategy for Documentation-as-UI

**Learning:** In documentation-only repositories, the README.md serves as the primary User Interface. Standard web metrics like LCP translate to Time-to-Content (TTC), while TTI translates to Time-to-Action (TTA). Providing a direct 'Fast View' link to a Google Sheets 'pubhtml' export (~9KB) reduces the initial data access payload by ~97% compared to the full spreadsheet editor UI (~300KB+).

**Action:** Prioritize 'Fast View' links and inlined previews of critical data to minimize TTC and TTA. Use semantic HTML and status badges to provide immediate scannable metadata.
