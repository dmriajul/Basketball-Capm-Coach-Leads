# Bolt's Performance Journal ⚡

## 2024-05-22 - Payload Optimization for Document-Centric Repos
**Learning:** In repositories where the primary value is external data (e.g., Google Sheets), the "Time-to-Content" bottleneck is the heavy editor interface (~320KB). Bypassing this with inline Markdown previews and Published Web Views (pubhtml, ~9KB) reduces the initial payload by >95%.
**Action:** Always provide a "Quick Preview" and "Fast View" link to optimize data accessibility.
