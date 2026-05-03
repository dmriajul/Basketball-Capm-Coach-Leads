## 2026-05-01 - Optimizing Documentation-as-UI (TTC/TTA)

**Learning:** In documentation-centric repositories, the README.md is the primary User Interface. Traditional code optimizations (like O(n) vs O(n^2)) are less impactful than optimizations for Time-to-Content (TTC) and Time-to-Action (TTA). Reducing data access payload (e.g., using Google Sheets `pubhtml` vs the full editor) can reduce the initial payload by ~97%.

**Action:** Prioritize 'Fast View' links and 'Zero-Latency Previews' (inlined data) in the README to provide immediate value and reduce dependency on external, heavy UI-loading services.
