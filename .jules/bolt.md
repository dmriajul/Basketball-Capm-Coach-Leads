## 2026-05-31 - Optimization Strategy for Documentation-only Repos
**Learning:** In repositories where the README acts as the primary interface, performance is measured by Time-to-Content (TTC) and Time-to-Action (TTA). Providing a direct 'Fast View' link to the Google Sheets 'pubhtml' export (~9KB) reduces the initial data access payload by ~97% compared to the full spreadsheet editor UI (~300KB+).
**Action:** Replace or supplement heavy editor links with lightweight 'pubhtml' exports and include inlined previews of critical data to minimize TTA.

## 2026-05-31 - Data Source of Truth
**Learning:** Local CSV data (like `leads.csv`) may be outdated. The May 2026 staff roster (Jason Kidd, Latricia Trammell, Max Hooper, Andy Enfield, Jamie Dixon) is the verified technical source of truth for the preview table.
**Action:** Prioritize verified roster data over local artifacts for README previews.
