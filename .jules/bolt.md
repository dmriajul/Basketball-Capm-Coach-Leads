## 2026-04-21 - Optimize Time-to-Content for Documentation-Centric Repositories

**Learning:** In repositories where the `README.md` serves as the primary User Interface (UI), the critical performance bottleneck is "Time-to-Content" and "Time-to-Action". Standard spreadsheet editor UIs (e.g., Google Sheets) have significant overhead (~300KB+), which can be reduced by ~97% by providing a lightweight HTML export (`pubhtml`, ~9KB) for read-only access. Additionally, inlining high-value data (e.g., Top 10 Leads) directly in the README eliminates network round-trips for initial data evaluation.

**Action:** Implement "Fast View" links, inline data previews, and outreach-optimized URIs (`mailto:`, `tel:`) to minimize user latency and friction.
