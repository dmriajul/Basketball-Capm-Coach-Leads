## 2025-05-14 - [GitHub Markdown Header Anchor Generation]
**Learning:** GitHub's automatic anchor generation for headers (`# Heading`) strips emojis, parentheses, and most special characters from the resulting ID. For example, `# ⚡ Quick Preview` becomes `#quick-preview`.
**Action:** When creating internal document links, ensure the fragment matches the cleaned version of the header text to avoid broken navigation.
