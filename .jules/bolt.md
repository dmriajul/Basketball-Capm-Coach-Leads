## 2026-04-29 - Initializing Documentation Performance Strategy
**Learning:** In documentation-centric repositories where the README acts as the primary UI, performance is measured by Time-to-Content (TTC) and Time-to-Action (TTA). External dependencies (like full Google Sheets UI) introduce significant latency (~300KB+ payload).
**Action:** Use `pubhtml` exports for a ~97% reduction in payload (~9KB) and inline critical data segments (Top 5 Leads) to achieve zero-latency initial data discovery.
