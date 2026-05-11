# 🏀 Basketball-Camp-Coach-Leads

[![Leads Count](https://img.shields.io/badge/Leads-100+-blue.svg)](https://docs.google.com/spreadsheets/d/15aaf3T3SSK_JptoitO8avud5TEzp0EEtZERNa9MAR-8/)
[![Last Updated](https://img.shields.io/badge/Last_Updated-May_2026-green.svg)](https://github.com/Riajul-Khandokar/Basketball-Capm-Coach-Leads)

> High-quality basketball coaching leads for camps, clinics, and recruitment outreach.

## ⚡ Performance Access
- **[🚀 Fast View (HTML)](https://docs.google.com/spreadsheets/d/15aaf3T3SSK_JptoitO8avud5TEzp0EEtZERNa9MAR-8/pubhtml)**: Lowest latency (~9KB), zero-auth required.
- **[📊 Full Editor (Google Sheets)](https://docs.google.com/spreadsheets/d/15aaf3T3SSK_JptoitO8avud5TEzp0EEtZERNa9MAR-8/)**: For data entry and advanced filtering (~300KB+).

## 🔍 Zero-Latency Preview (Top 5 Leads)
Instant access to primary contacts without leaving the repository.

| Camp / Organization | Team | Coach / Contact | Action |
| :--- | :--- | :--- | :--- |
| NBA Scouting | Dallas Mavericks | Rick Carlisle | [📧 Email](mailto:rcarlisle@dogwoodequity.com) |
| WNBA Outreach | Dallas Wings | Vickie Johnson | [📧 Email](mailto:vjohnson@lasvegasaces.com) |
| G-League Prep | Texas Legends | David Arseneault | — |
| NCAA DI Prospect | SMU Mustangs | Tim Jankovich | — |
| NCAA DI Clinic | TCU Horned Frogs | Jamie Dixon | — |

## 🛠️ Data Management
The repository includes scripts for maintaining data integrity and performance.

### `clean_leads.py`
Optimized Python script for high-throughput deduplication and normalization.
- **Performance:** Processes ~480k rows/sec.
- **Optimizations:** LRU caching, hot-loop bypass for sparse data, atomic file replacement.

---
*Last updated: May 2026*
