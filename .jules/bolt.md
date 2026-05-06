## 2026-05-04 - Prioritizing TTC and TTA in Documentation-Centric Repositories
**Learning:** In repositories where the README.md acts as the primary user interface, performance is best measured by Time-to-Content (TTC) and Time-to-Action (TTA). Large external payloads (e.g., the full Google Sheets editor UI) significantly degrade the user experience.
**Action:** Implement zero-latency data previews using inlined Markdown tables and provide optimized "Fast View" links (e.g., pubhtml) to reduce payloads and eliminate initialization bottlenecks.
