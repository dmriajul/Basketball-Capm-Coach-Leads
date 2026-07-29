# Bolt's Journal - Critical Learnings Only

## 2026-07-08 - Data Access Optimization and Zero-Latency Previews
**Learning:** Inlined datasets in documentation-only repositories provide immediate zero-latency previews, reducing Time-to-Action (TTA) and payload sizes compared to external Google Sheets. Exact counts of HTML semantic tags (<abbr>, mailto:, tel:, <kbd>) must match required numbers precisely.
**Action:** Always verify Markdown tag counts using a local Python script and ensure no HTML/link elements inside Markdown table cells are wrapped in backticks.
