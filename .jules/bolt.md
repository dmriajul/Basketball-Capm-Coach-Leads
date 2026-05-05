## 2026-05-04 - [Optimization: Time-to-Content for Data Repositories]
**Learning:** For documentation-centric repositories where the README acts as the primary UI, Time-to-Content (TTC) and Time-to-Action (TTA) are the most critical performance metrics. Providing a direct 'Fast View' link to a Google Sheets 'pubhtml' export (~9KB) reduces the initial payload by ~97% compared to the full spreadsheet editor (~300KB+).
**Action:** Always prioritize inlined zero-latency previews and high-performance 'pubhtml' links for read-only data access.
