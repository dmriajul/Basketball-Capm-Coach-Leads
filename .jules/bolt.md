# Bolt Journal - Basketball Camp Coach Leads

## 2026-04-29 - Payload Reduction via Spreadsheet 'pubhtml'
**Learning:** For read-only users, providing a link to the Google Sheets 'pubhtml' export (~9KB) reduces the initial data access payload by ~97% compared to the full spreadsheet editor UI (~300KB+).
**Action:** Use the `pubhtml` URL for 'Fast View' links to significantly improve Time-to-Content (TTC).

## 2026-05-01 - Zero-Latency Preview for Lead Discovery
**Learning:** Inlining a 'Top 5 Leads' table directly in the README eliminates the 'Time-to-Content' bottleneck of external network requests for the most common use case (initial discovery).
**Action:** Include an accessible, thematic preview table in the README to provide immediate value.

## 2026-05-04 - Documentation-Centric Performance Strategy
**Learning:** In repositories where the README is the primary UI, Time-to-Content (TTC) and Time-to-Action (TTA) are the most critical performance metrics. Payload reduction and direct outreach links (mailto/tel) are more effective than code-level micro-optimizations.
**Action:** Prioritize layout efficiency, metadata scannability (badges), and direct action links in documentation updates.
