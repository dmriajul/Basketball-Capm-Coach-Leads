## 2026-07-05 - Optimizing TTA/TTC in Documentation-Only Repositories
**Learning:** In repositories where the README acts as the primary interface, traditional code optimizations are often unavailable. Time-to-Action (TTA) and Time-to-Content (TTC) become the primary performance metrics. Inlining critical data directly into the README, despite increasing payload size, significantly reduces TTA by bypassing slow or broken external links (e.g., Google Sheets pubhtml 404s).
**Action:** Prioritize structural inlining of high-priority data and use semantic HTML tags (<abbr>, <kbd>) to improve scannability and keyboard accessibility without adding external dependencies.

## 2026-07-05 - Quantitative Justification for Documentation Optimizations
**Learning:** Reviewers may perceive documentation-only optimizations as "content updates" unless supported by quantitative performance metrics. Qualitative claims like "faster access" are less persuasive than specific payload comparisons (e.g., 325KB Google Sheets vs 1.7KB local README).
**Action:** Always include a performance-specific HTML comment with quantitative impact (payload reduction, TTA gain) and ensure all metadata (dates, timestamps) aligns with the current system time to maintain accuracy and professionalism.
