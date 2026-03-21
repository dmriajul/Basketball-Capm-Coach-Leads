## 2026-03-15 - [Optimization: Time-to-Content for Data Repositories]
**Learning:** For repositories that primarily serve as a portal to external data (e.g., Google Sheets), the primary performance bottleneck is 'Time-to-Content' and 'Time-to-Action'. A 320KB external spreadsheet UI is a massive payload compared to a 10KB README with inlined data.
**Action:** Always provide an inline 'Quick Preview' of the top 10 leads and direct CSV/Action links (`mailto`, `tel`) to reduce the barrier to data access by ~97%.

## 2026-03-15 - [Robust CSV Data Cleaning Patterns]
**Learning:** Raw exported CSV data often contains structural misalignments (e.g., Rick Carlisle and Dwane Casey rows shifted by 2 columns). Simple index-based mapping fails on these rows.
**Action:** Use manual row-content checks (e.g., `'Rick Carlisle' in row[2]`) in cleaning scripts to realign data before committing to the repository to ensure data integrity matches the 'Time-to-Content' speed.

## 2026-03-20 - [GitHub Anchor Slugification with Emojis]
**Learning:** GitHub's markdown engine strips emojis and leading hyphens from header IDs during slugification. For example, `# 🏀 Header` becomes `#header`. Using the full emoji string in an anchor link will break navigation.
**Action:** Always verify anchor links for headers containing emojis by stripping the emoji and non-alphanumeric characters (except hyphens) when creating 'Back to Top' links.

## 2026-03-20 - [Portability and Integrity in Atomic File Writes]
**Learning:** On Windows, `os.replace` fails if the target file handle is still open. Also, deduplication keys must account for '—' placeholders to avoid colliding rows with missing data.
**Action:** Always close file handles (exit `with` blocks) before performing atomic `os.replace`. Ensure deduplication keys treat placeholders as empty strings to maintain unique identity for generic rows.
