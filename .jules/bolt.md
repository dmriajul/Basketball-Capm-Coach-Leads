## 2026-06-15 - Optimizing Documentation-as-UI
**Learning:** In repositories where the README is the primary interface, performance bottlenecks are often related to Time-to-Content (TTC) and Time-to-Action (TTA). Standard Google Sheets editor links incur significant payload (~325KB) compared to `pubhtml` exports (~3KB).
**Action:** Replace heavy external links with lightweight `pubhtml` views and inline critical data to provide instant access and reduce network latency.
