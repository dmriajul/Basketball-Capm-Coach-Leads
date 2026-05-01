## 2026-05-01 - Time-to-Content Optimization for Documentation-Only Repos

**Learning:** In documentation-centric projects where the README acts as the primary UI, 'Time-to-Content' (TTC) and 'Time-to-Action' (TTA) are the most critical performance metrics. Inlining high-value data segments directly within the README provides a zero-latency 'Quick Preview' that eliminates the bottleneck of external network requests and heavy third-party UI initialization. Furthermore, providing a direct 'Fast View' link to a Google Sheets 'pubhtml' export (~9KB) reduces the initial data access payload by ~97% compared to the full spreadsheet editor UI (~300KB+).

**Action:** Always provide zero-latency data previews and lightweight 'Fast View' links in documentation-only repositories to minimize TTC and TTA for read-only users.
