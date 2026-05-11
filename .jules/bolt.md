# ⚡ Bolt Performance Journal

This journal documents critical performance learnings and optimizations specific to the Basketball Camp Coach Leads repository.

## 2026-05-04 - Zero-Latency Data Previews
**Learning:** Inlining high-value data segments (e.g., Top 5 Leads) directly within the README provides a zero-latency 'Quick Preview' that eliminates the 'Time-to-Content' (TTC) bottleneck of external network requests and heavy third-party UI initialization.
**Action:** Always provide a curated subset of critical data in the primary README for instant access.

## 2026-05-04 - Fast View Optimization
**Learning:** Providing a direct 'Fast View' link to the Google Sheets 'pubhtml' export (~9KB) reduces the initial data access payload by ~97% compared to the full spreadsheet editor UI (~300KB+), significantly improving TTC and TTA (Time-to-Action) for read-only users.
**Action:** Prioritize lightweight 'pubhtml' links over heavy interactive editor links in documentation-only environments.

## 2026-05-04 - Hot Loop Efficiency in clean_leads.py
**Learning:** In clean_leads.py, increasing the lru_cache for get_dedupe_key to 16384 and implementing conditional bypass logic in the hot loop to skip clean_url and clean_field function calls for empty or placeholder values significantly reduces overhead for sparse datasets.
**Action:** Use conditional checks to bypass function calls for known placeholders or empty strings in high-frequency loops.
