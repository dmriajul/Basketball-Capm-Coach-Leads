# Bolt ⚡ Journal - Performance Learnings

## 2026-05-18 - Documentation as a User Interface (UI)
**Learning:** In documentation-only repositories, the primary performance metrics are Time-to-Content (TTC) and Time-to-Action (TTA). External links to heavy spreadsheet editors (~300KB+) create significant latency. Inlining a "Fast Path" preview and using `pubhtml` exports (~9KB) can reduce the initial data access payload by ~97%.
**Action:** Always provide zero-latency inlined previews for the top 5 records and a direct link to the lightweight `pubhtml` version of the data source.
