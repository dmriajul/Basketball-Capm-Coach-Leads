## 2026-05-26 - Documentation-as-UI Performance Strategy
**Learning:** In documentation-only repositories, the README.md is the primary User Interface. Standard performance metrics like Time-to-Content (TTC) and Time-to-Action (TTA) apply. Using Google Sheets 'pubhtml' exports reduces the initial data access payload by ~97% (~9KB vs ~300KB+) compared to the full spreadsheet editor UI.
**Action:** Prioritize 'Fast View' pubhtml links and inlined previews with emoji-prefixed contact actions to minimize TTA and TTC.
