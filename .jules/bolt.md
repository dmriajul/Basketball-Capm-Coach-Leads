## 2026-05-15 - Optimizing Documentation-as-UI
**Learning:** In repositories where the README.md is the primary interface, 'Time-to-Content' (TTC) and 'Time-to-Action' (TTA) are the most critical performance metrics. Providing a direct 'Fast View' link to a Google Sheets 'pubhtml' export (~9KB) instead of the full editor UI (~300KB+) reduces the payload by ~97%.
**Action:** Always prioritize inlining high-value data segments (Top 5 leads) for zero-latency previews and using 'pubhtml' links for external data access.
