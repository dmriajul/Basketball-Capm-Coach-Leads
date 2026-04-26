## 2026-04-21 - Documentation Performance Strategy
**Learning:** In documentation-centric repositories where the README is the primary UI, performance is measured by Time-to-Content (TTC) and Time-to-Action (TTA). External spreadsheets and heavy UI wrappers (like the full Google Sheets editor) introduce significant bottlenecks (~300KB+ payload).
**Action:** Implement "Zero-Latency" data previews by inlining high-value data segments directly in the README and provide "Fast-View" links (pubhtml) to reduce payload by ~97% (~9KB vs ~300KB).
