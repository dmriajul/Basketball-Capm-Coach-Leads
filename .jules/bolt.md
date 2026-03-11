## 2024-03-11 - Optimizing Documentation-Centric Repositories

**Learning:** In repositories where the primary value is data stored in external spreadsheets, "performance" is defined by Time-to-Content and Time-to-Action. Bypassing heavy editor interfaces (like Google Sheets' /edit view, which is ~320KB) in favor of Published Web Views (/pubhtml, ~9KB) or direct CSV/PDF downloads provides a significant speed boost for end-users. Additionally, providing an inline "Quick Preview" of the data within the README.md reduces Time-to-Content to nearly zero.

**Action:** Always provide lightweight alternative access methods (pubhtml, CSV, PDF) and inline previews for data-heavy documentation projects. Use `mailto:` and `tel:` links to speed up user actions.
