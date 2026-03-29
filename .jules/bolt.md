## 2026-03-25 - [Deduplication and Placeholder Optimization]
**Learning:** Performing deduplication checks *before* expensive string operations (like `strip()`, `lower()`, or `normalize_url`) significantly improves performance, especially on large datasets with repeats or missing data. Fast-path checks for known placeholders (e.g., '—') further reduce CPU cycles by skipping redundant processing.
**Action:** Always structure processing pipelines to 'fail fast' and skip work for duplicate or empty rows as early as possible.

## 2026-03-25 - [URL Normalization Memoization]
**Learning:** URL normalization (upgrading http to https and adding protocols) is often redundant across large datasets (e.g., multiple coaches from the same team website). Using `functools.lru_cache(maxsize=None)` for these pure functions yields a massive speedup by eliminating repeated string manipulations.
**Action:** Use memoization for idempotent string cleaning and normalization functions in data processing scripts.
