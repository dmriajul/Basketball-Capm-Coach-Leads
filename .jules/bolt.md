## 2026-05-22 - Optimization Strategy for Documentation-Centric Repository

**Learning:** In a repository where the README.md serves as the primary User Interface (UI), performance is best measured by Time-to-Content (TTC) and Time-to-Action (TTA). The default Google Sheets editor UI is heavy (~300KB+) and introduces significant latency. Using the `pubhtml` export reduces the payload to ~9KB (a ~97% reduction).

**Action:** Implement "Fast View" links using Google Sheets `pubhtml` and provide inlined "Top 5 Leads" previews to eliminate initial network latency for data discovery.
