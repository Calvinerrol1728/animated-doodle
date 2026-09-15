# Recruit Monitoring & Pipeline Tracker

A professional, comprehensive Excel workbook and automated registration system designed for agency leaders, unit managers, and recruiters to track candidates through the recruitment funnel, specifically focusing on **Complete Name**, **ADD (Agency Discovery Day / Career Orientation) Attendance**, and **LMS (Learning Management System Training) Completion**.

---

## 🌟 What's New: Automated ADD Registration Form

Recruits can now register themselves online! When a candidate submits the registration form, they are **automatically added into your Excel sheet (`Recruit_Monitoring_Tracker.xlsx`)** in real-time.

### How It Works:
1. **Candidate Fills Form:** The recruit opens the online registration form (`/register`).
2. **They Enter Details:** Complete Name, Contact Number, Email Address, Who Invited Them (Recruiter), Preferred ADD Date, and Career Goals.
3. **Instant Auto-Save to Excel:** The system assigns a Recruit ID (`REC-007`, etc.), appends the candidate to the first available row in `Recruit_Monitoring_Tracker.xlsx`, sets **Attended ADD?** to `Pending`, sets **Completed LMS?** to `Not Started`, and sets the automated stage to `ADD Scheduled`.
4. **Real-time Synchronization:** The main dashboard, top KPI cards, and CSV export reflect the new recruit immediately.

---

## 📁 Files Included

| File | Description |
| :--- | :--- |
| **`Recruit_Monitoring_Tracker.xlsx`** | **The main Excel deliverable**: A fully styled, multi-sheet workbook with formulas, KPI cards, charts, conditional formatting, and data validation dropdowns. |
| **`register.html`** | The candidate-facing, mobile-friendly ADD registration web form. |
| **`index.html`** | The executive monitoring dashboard with real-time search, filters, KPI cards, and direct form integration. |
| **`server.py`** | Background Python server that serves the dashboard and handles form submissions by appending recruits directly to Excel. |
| **`Recruit_Monitoring_Export.csv`** | CSV export containing candidate records for quick import/export. |
| **`build_tracker.py`** | Standalone Python generator script using `openpyxl` to build or customize the workbook. |

---

## 👥 Current Encoded Roster (All 6 Attended ADD Sept 14, 2026)

| ID | Complete Name | Attended ADD? | ADD Date | Completed LMS? | LMS Access Date | Pipeline Stage | Next Action Required |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **REC-001** | **Grandes, Maybe** | `Yes` | 2026-09-14 | `In Progress` | 2026-09-15 | `LMS In Progress` | Process LMS portal registration & send login access link today |
| **REC-002** | **Bagiuos, Michael** | `Yes` | 2026-09-14 | `Not Started` | — | `ADD Attended - Awaiting LMS` | Follow up on ADD feedback & check readiness to process LMS |
| **REC-003** | **Barilea, Alona** | `Yes` | 2026-09-14 | `Not Started` | — | `ADD Attended - Awaiting LMS` | Follow up on ADD feedback & check readiness to process LMS |
| **REC-004** | **Garrucha, Lorenz** | `Yes` | 2026-09-14 | `Not Started` | — | `ADD Attended - Awaiting LMS` | Follow up on ADD feedback & check readiness to process LMS |
| **REC-005** | **Ambos, Princess** | `Yes` | 2026-09-14 | `Not Started` | — | `ADD Attended - Awaiting LMS` | Follow up on ADD feedback & check readiness to process LMS |
| **REC-006** | **Montano, Jezreel Kate** | `Yes` | 2026-09-14 | `Not Started` | — | `ADD Attended - Awaiting LMS` | Follow up on ADD feedback & check readiness to process LMS |

*New registrants from the online form will automatically be added as `REC-007` on row 15.*

---

## 📊 Workbook Structure (4 Dedicated Sheets)

1. **`Recruit Monitoring Tracker`** (Main tracking sheet with Top KPI Cards, candidate details, ADD attendance, LMS completion, and automated pipeline stage formulas).
2. **`Recruitment Dashboard`** (Funnel conversion analysis, column chart, status breakdown tables, LMS pie chart, and recruiter performance roster).
3. **`Dropdowns & Settings`** (Reference lists and glossary for dropdown menus).
4. **`User Guide & Workflow`** (Operating manual and insurance recruitment best practices).

---

## 🚀 How to Share the Registration Form with Recruits

1. **In Live Preview:** Click the **"Copy Shareable Link"** button in the dashboard preview banner.
2. **Send to Candidates:** Paste the link into WhatsApp, Viber, Messenger, or SMS:
   > *"Hi! Please fill out our brief Agency Discovery Day (ADD) registration form to confirm your orientation slot: [your-link]/register"*
3. **Automatic Logging:** Once they submit, check your Excel sheet or dashboard — the candidate appears automatically!
