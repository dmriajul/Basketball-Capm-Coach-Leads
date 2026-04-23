## 2026-04-21 - Documentation-Centric Performance Strategy
**Learning:** In repositories where the README is the primary interface, traditional backend/frontend metrics shift to "Time-to-Content" and "Time-to-Action". Standard spreadsheet editor UIs (~300KB) are massive bottlenecks compared to HTML exports (~9KB).
**Action:** Prioritize zero-latency data previews via inlined tables and leverage Google Sheets 'pubhtml' exports for a ~97% reduction in initial data access payload.
