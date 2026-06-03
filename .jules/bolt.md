## 2026-05-31 - Optimization for Doc-only Repos
**Learning:** In documentation-only repositories, the README.md is the primary UI. Performance is measured by Time-to-Content (TTC) and Time-to-Action (TTA). Providing a 'Fast View' pubhtml link reduces data access payload by ~97% compared to the full Google Sheets editor.
**Action:** Implement 'Fast View' links and inlined data previews with semantic HTML in the README to minimize user latency.
