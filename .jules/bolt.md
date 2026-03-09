# Bolt's Journal - Performance Optimizations

## 2024-05-22 - Optimizing Time-to-Content for Documentation-Centric Repositories
**Learning:** In repositories where the primary "product" is external data (e.g., Google Sheets), the standard editor interface is a performance bottleneck (~320KB payload). Users often just need to view or download the data.
**Action:** Provide "Fast View" (pubhtml, ~9KB) and direct export links (CSV/PDF) to bypass the heavy editor UI.
