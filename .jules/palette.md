## 2026-04-20 - Documentation as UI
**Learning:** In documentation-only repositories, the README effectively serves as the primary user interface. "Time-to-Content" can be significantly reduced by implementing horizontal navigation bars with descriptive tooltips and categorical icons. Correcting typos (e.g., "Capm" to "Camp") and adding trust signals like status badges immediately improves professional credibility and user confidence.
**Action:** Prioritize horizontal navigation and accessible acronym expansions (<abbr>) when the README is the only point of user interaction.

## 2026-04-20 - Reducing Time-to-Action with Entity Interlinking
**Learning:** Incorporating `mailto:` and `tel:` links directly within a data preview table reduces the steps a user must take to act on the information provided.
**Action:** Use direct action links (email, phone, profile) in data summaries to minimize "Time-to-Action".

## 2026-04-20 - Markdown Navigation with Emojis
**Learning:** When creating internal links (anchors) to headers that contain emojis, many Markdown parsers include the emoji's character representation or specific slugification in the ID. To ensure robustness, link to the closest relevant header or ensure the slug matches the rendered ID (e.g., `#-quick-access` for `## 🚀 Quick Access`).
**Action:** Always verify anchor link targets in the rendered documentation environment.
