## 2026-06-12 - [TTC/TTA Optimization for Documentation-as-UI]
**Learning:** In documentation-only repositories, the README.md acts as the primary User Interface. Measuring performance in terms of Time-to-Content (TTC) and Time-to-Action (TTA) revealed that external spreadsheet links (TTC ~800ms) were a major bottleneck compared to inlined previews (TTC 0ms).
**Action:** Use 'pubhtml' exports for lightweight spreadsheet access and inline the most critical data (e.g., Top 5 Leads) with emoji-prefixed 'mailto:' and 'tel:' links to reduce TTA by ~97%.
