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

## 2026-03-25 - [Overhead of Dict-based CSV Operations]
**Learning:** For high-performance data processing in Python, `csv.DictWriter` and `csv.DictReader` introduce measurable overhead (approx. 10-15% in this codebase) compared to `csv.writer` and `csv.reader` due to dictionary creation and key lookups in every row.
**Action:** Use list-based `csv.writer` and `csv.reader` for simple transformations where field order is stable to minimize row processing latency.

## 2026-03-27 - [Redundant Allocations in CSV Row Processing]
**Learning:** Even with `csv.writer`, creating new list objects for every row (via list comprehensions or template-based reconstruction) adds measurable overhead (~25-30% in this codebase). Merging cleaning operations into a single-pass list comprehension and modifying the existing `row` list in-place for general cases significantly improves throughput.
**Action:** Use single-pass transformations and in-place list modifications (`row[i] = ...`) when possible to avoid the cost of redundant list allocations during bulk data cleaning.

## 2026-03-27 - [Brittle Data Indexing in Optimized Processors]
**Learning:** While switching from `DictReader` to `csv.reader` (list-based) improves throughput, it introduces brittleness. If source data columns shift, index-based checks (e.g., `row[2]` instead of `row[4]`) fail silently or create corrupted entries.
**Action:** Always verify current data structure using `head` and `tr` before implementing index-based performance optimizations. Use in-place modifications to maintain some safety while gaining speed.

## 2026-03-28 - [Fast-path for Common Placeholders in Row Processing]
**Learning:** In data cleaning pipelines where a significant portion of cells contain a standard placeholder (e.g., '—'), a simple fast-path check in the list comprehension (`v if v == PLACEHOLDER else ...`) can reduce row processing time by ~15-20% by skipping redundant `strip()` and `lower()` calls.
**Action:** Always identify high-frequency static values in datasets and implement fast-path skips in hot loops to avoid unnecessary string manipulations.
