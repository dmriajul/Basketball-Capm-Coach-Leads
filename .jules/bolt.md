## 2026-05-14 - Payload Reduction via Lightweight HTML Export
**Learning:** In documentation-centric repositories where the README.md is the primary UI, providing a direct 'Fast View' link to Google Sheets 'pubhtml' export (~9KB) reduces the initial data access payload by ~97% compared to the full editor (~300KB+), significantly improving Time-to-Content (TTC).
**Action:** Prioritize lightweight read-only views for external datasets to minimize user-perceived latency.

## 2026-05-14 - Zero-Latency Data Previews
**Learning:** Inlining high-value data segments (e.g., Top 5 Leads) directly within the README eliminates the TTC bottleneck of external network requests and third-party UI initialization.
**Action:** Implement 'Quick Preview' tables in READMEs to provide immediate value and reduce Time-to-Action (TTA).
