## 2026-07-08 - Optimizing Data Access Efficiency in Documentation-Only Repositories

**Learning:** In repositories where the primary interface is the README, relying on external, heavy editor links (e.g., Google Sheets) creates a significant "Time-to-Action" (TTA) bottleneck due to high payload sizes (~325KB) and slow network latency. Structural optimizations that inline verified data using semantic HTML and GitHub-native features can reduce TTA and payload size (~1.7KB) by 99% while maintaining accessibility.

**Action:** Identify critical roster or lead data currently hosted externally. Replace or supplement with an inlined, scannable table using `<abbr>` for tooltips, `mailto:` and `tel:` protocols for direct action, and `<kbd>` for shortcut hints. Always justify the technical impact in performance comments.
