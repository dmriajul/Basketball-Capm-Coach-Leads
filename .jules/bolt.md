## 2026-05-19 - Documentation as UI Performance
**Learning:** In documentation-only repositories, the README.md is the primary User Interface. Standard performance metrics like bundle size are less relevant than Time-to-Content (TTC) and Time-to-Action (TTA). Using Google Sheets 'pubhtml' export (~9KB) instead of the full editor (~300KB) reduces the data access payload by ~97%.
**Action:** Prioritize 'Fast View' pubhtml links and zero-latency inlined previews (Top 5 rows) in READMEs to minimize TTA.
