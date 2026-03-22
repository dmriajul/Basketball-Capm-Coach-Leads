## 2026-03-15 - [Optimization: Time-to-Content for Data Repositories]
**Learning:** For repositories that primarily serve as a portal to external data (e.g., Google Sheets), the primary performance bottleneck is 'Time-to-Content' and 'Time-to-Action'. A 320KB external spreadsheet UI is a massive payload compared to a 10KB README with inlined data.
**Action:** Always provide an inline 'Quick Preview' of the top 10 leads and direct CSV/Action links (`mailto`, `tel`) to reduce the barrier to data access by ~97%.

## 2026-03-15 - [Robust CSV Data Cleaning Patterns]
**Learning:** Raw exported CSV data often contains structural misalignments (e.g., Rick Carlisle and Dwane Casey rows shifted by 2 columns). Simple index-based mapping fails on these rows.
**Action:** Use manual row-content checks (e.g., `'Rick Carlisle' in row[2]`) in cleaning scripts to realign data before committing to the repository to ensure data integrity matches the 'Time-to-Content' speed.

## 2026-03-20 - [GitHub Anchor Slugification with Emojis]
**Learning:** GitHub's markdown engine strips emojis and leading hyphens from header IDs during slugification. For example, `# 🏀 Header` becomes `#header`. Using the full emoji string in an anchor link will break navigation.
**Action:** Always verify anchor links for headers containing emojis by stripping the emoji and non-alphanumeric characters (except hyphens) when creating 'Back to Top' links.

## 2026-03-20 - [Optimization: Bypassing Heavy UI Wrappers for Data Access]
**Learning:** GitHub's default CSV viewer can take several seconds to render for larger files, significantly increasing "Time-to-Content" for raw data access. Appending `?raw=true` to the link bypasses this rendering layer entirely.
**Action:** Always use `?raw=true` for direct data download links in documentation to ensure immediate file availability.

## 2026-03-20 - [Performance: Memoization in Data Pipelines]
**Learning:** In text-heavy data processing scripts, common strings and URLs are often repeated. Using `functools.lru_cache` on normalization and cleaning functions reduces CPU cycles by avoiding redundant string operations and regex/prefix checks.
**Action:** Implement memoization for deterministic string transformation functions in data processing scripts to optimize for O(unique_items) instead of O(total_items).
