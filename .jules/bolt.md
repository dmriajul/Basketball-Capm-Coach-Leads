## 2026-05-20 - Payload Optimization via pubhtml
**Learning:** Standard Google Sheets editor links are heavy (~2-3MB). Using `pubhtml` exports reduces the initial payload to ~80KB (a 97% reduction), significantly improving Time-to-Content (TTC).
**Action:** Always prefer `pubhtml` for read-only directory access in documentation-only repositories to optimize TTA and TTC.
