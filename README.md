# Recruit Monitoring & Pipeline Tracker

A professional, comprehensive Excel workbook designed for agency leaders, unit managers, and recruiters to track candidates through the recruitment funnel, specifically focusing on **Complete Name**, **ADD (Agency Discovery Day / Career Orientation) Attendance**, and **LMS (Learning Management System Training) Completion**.

---

## 📁 Files Included

| File | Description |
| :--- | :--- |
| **`Recruit_Monitoring_Tracker.xlsx`** | **The main deliverable**: A fully styled, multi-sheet Excel workbook with formulas, KPI cards, charts, conditional formatting, and data validation dropdowns. |
| **`Recruit_Monitoring_Export.csv`** | CSV export containing the header structure and 15 sample candidate records for quick import/export. |
| **`build_tracker.py`** | Standalone Python generator script using `openpyxl` to build or customize the workbook. |
| **`server.py` & `index.html`** | Interactive web dashboard providing live browser preview, real-time search, filter tabs, and direct `.xlsx` download. |

---

## 📊 Workbook Structure (4 Dedicated Sheets)

### 1. `Recruit Monitoring Tracker` (Main Tracking Sheet)
- **Executive KPI Cards (Rows 4–6)**:
  - **Total Recruits Tracked**: `=COUNTA(B9:B65)` (Real-time count of active candidates)
  - **Attended ADD**: `=COUNTIF(H9:H65, "Yes")` with automated Attendance Rate %
  - **LMS In Progress**: `=COUNTIF(L9:L65, "In Progress")` (Candidates currently taking modules)
  - **Completed LMS**: `=COUNTIF(L9:L65, "Yes")` with Completion Rate % among ADD attendees
  - **Funnel Conversion Rate**: `=IFERROR(COUNTIF(L9:L65,"Yes")/COUNTA(B9:B65), 0)` (Total recruits to certified agents)
- **Table Columns (19 Comprehensive Columns)**:
  - **A: Recruit ID** — Auto-generated (`REC-001`, `REC-002`, etc.) via formula for new rows.
  - **B: Complete Name** — Candidate's full name (*Last Name, First Name M.I.*).
  - **C: Contact Number** — Mobile phone number.
  - **D: Email Address** — Email used for calendar invites & LMS accounts.
  - **E: Sourced By** — Recruiter, unit manager, or team member name.
  - **F: Date Sourced** — Date candidate entered the pipeline (`YYYY-MM-DD`).
  - **G: ADD Scheduled Date** — Date of the scheduled Agency Discovery Day seminar.
  - **H: Attended ADD?** — Data validation dropdown (`Yes`, `No`, `Rescheduled`, `Pending`) with color-coding.
  - **I: ADD Attendance Date** — Actual date attended.
  - **J: ADD Remarks / Feedback** — Candidate interest level, questions, or notes.
  - **K: LMS Access Date** — Date credentials were provided to the recruit.
  - **L: Completed LMS?** — Data validation dropdown (`Yes`, `In Progress`, `Not Started`, `Withdrawn`) with color-coding.
  - **M: LMS Completion Date** — Date all modules and assessments were finished.
  - **N: LMS Progress %** — Formatted percentage (e.g., `100%`, `75%`, `50%`, `0%`).
  - **O: LMS Score / Certificate** — Certificate number or mock test score.
  - **P: Current Pipeline Stage** — **Automated Formula** classifying candidate status in real-time.
  - **Q: Next Action Required** — Specific follow-up task (e.g., *Schedule Exam*, *Send LMS Link*).
  - **R: Target Follow-up Date** — Due date for next recruiter outreach.
  - **S: Recruiter Notes** — Ongoing comments and candidate notes.

- **Pre-formatted Rows (Rows 24–65)**:
  - 42 blank template rows equipped with dropdowns, cell borders, date formatting, and `=IF(B...="","",...)` formulas. As soon as you type a name into Column B, the Recruit ID and Pipeline Stage activate automatically.

---

### 2. `Recruitment Dashboard` (Executive Metrics & Funnel)
- **Pipeline Funnel Table**:
  - Stage 1: Recruits Sourced (100% baseline)
  - Stage 2: Attended ADD (% of total sourced)
  - Stage 3: Started LMS (% of ADD attendees)
  - Stage 4: Completed LMS (% of ADD attendees)
  - Stage 5: Ready for Licensing Exam (% certified and ready)
- **Embedded Column Chart**: Visual bar chart tracking pipeline milestone drop-off.
- **ADD Attendance Breakdown**: Summary counts and % shares for *Attended*, *Pending*, *Rescheduled*, and *Missed*.
- **LMS Completion Breakdown**: Summary counts and % shares for *Completed*, *In Progress*, *Not Started*, and *Withdrawn*, with an embedded **Pie Chart**.
- **Recruiter Performance Summary**: Team breakdown measuring individual recruiter volumes, attendance rates, LMS completion rates, and exam-ready candidates.

---

### 3. `Dropdowns & Settings` (Config & Reference Glossary)
- Reference lists and definitions for:
  - ADD Attendance status options
  - LMS Completion status options
  - Recruiter roster
  - Pipeline Stage definitions and triggering formulas

---

### 4. `User Guide & Workflow` (Operating Manual)
- Detailed instructions on the 4-step recruitment workflow.
- Explanation of key insurance recruitment acronyms (ADD, LMS, IC, UM).
- Recruiter best practices: The 24-Hour follow-up rule, the 7-to-10-day LMS momentum window, and re-scheduling protocols.

---

## 🎨 Design & Styling Highlights

- **Executive Navy & Ice Blue Theme**: Professional styling with dark navy headers (`#1B365D`), soft accent blue (`#2563EB`), and teal (`#0D9488`).
- **Freeze Panes**: Columns A & B (*Recruit ID* and *Complete Name*) remain fixed on screen as you scroll horizontally through ADD, LMS, and next steps.
- **Conditional Formatting**:
  - Green (`#D4EDDA`) for *Yes / Completed*
  - Amber (`#FFF3CD`) for *In Progress / Rescheduled*
  - Soft Red (`#F8D7DA`) for *No / Missed*
  - Soft Blue (`#DBEAFE`) for *Pending / Scheduled*
- **Gridlines Enabled**: Default sheet view explicitly displays Excel gridlines for readability.
- **Formulas with Error Handling**: All division formulas use `=IFERROR(..., 0)` to prevent `#DIV/0!` errors when rows are blank.

---

## 🚀 Quick Start Instructions

1. **Open the File**: Open `Recruit_Monitoring_Tracker.xlsx` in Microsoft Excel, Google Sheets, or LibreOffice Calc.
2. **Review Sample Data**: Explore rows 9 to 23 to see how formulas, dropdowns, and KPI cards operate with realistic candidates.
3. **Add Your Recruits**:
   - Scroll to row 24 (or overwrite sample rows).
   - Type candidate's name in **Column B (`Complete Name`)**.
   - Select **Col H (`Attended ADD?`)** and **Col L (`Completed LMS?`)** using the dropdown arrows.
   - Watch **Col P (`Current Pipeline Stage`)** and the **Top KPI Summary Cards** update automatically!
