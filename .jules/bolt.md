## 2026-07-08 - TTA/TTC Optimization in Documentation-Only Repos
**Learning:** In repositories where the README serves as the primary interface, performance bottlenecks manifest as Time-to-Action (TTA) and Time-to-Content (TTC). Inlining critical data (e.g., the July 2026 coaching roster) reduces the effective payload by ~99% (325KB external vs 1.7KB inlined) and eliminates the latency of external resource fetching.
**Action:** Prioritize "Zero-Latency" data previews and semantic HTML tags (<abbr>, <kbd>) to optimize for both speed and accessibility in documentation-centric projects.
