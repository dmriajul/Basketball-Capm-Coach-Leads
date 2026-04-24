## 2026-04-21 - Initial Performance Strategy for Documentation-Only Repo
**Learning:** In repositories where the README is the primary UI, performance is measured by 'Time-to-Content' (TTC) and 'Time-to-Action' (TTA). External links to heavy spreadsheet UIs are a bottleneck.
**Action:** Implement zero-latency data previews via inlined Markdown tables and provide 'Fast View' pubhtml links to minimize the initial data payload by ~97%.
