## 2026-06-11 - Optimized TTC/TTA for Doc-as-UI
**Learning:** In documentation-only repositories, the README.md is the User Interface. Performance is measured by Time-to-Content (TTC) and Time-to-Action (TTA). Heavy spreadsheet links can be replaced with lightweight `pubhtml` exports (reducing payload by ~97%) and inlined previews of critical data to minimize TTA.
**Action:** Use `pubhtml` for external data links and provide emoji-prefixed contact links with semantic `<abbr>` tags for high-speed scannability.
