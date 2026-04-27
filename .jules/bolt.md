## 2026-04-21 - Documentation-Centric Performance
**Learning:** In documentation-only repositories, the README acts as the primary UI. Traditional performance metrics (LCP, FID) translate to 'Time-to-Content' (TTC) and 'Time-to-Action' (TTA). Inlining data previews and using lightweight 'pubhtml' exports instead of full spreadsheet editors reduces initial payload by ~97%.
**Action:** Implement 'Fast View' pubhtml links and zero-latency inline previews to optimize TTC for read-only users.
