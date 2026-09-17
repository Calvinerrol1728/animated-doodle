import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

def add_recruiter_directory_tab(wb):
    ws = wb.create_sheet(title="Recruiter Directory & IDs")
    ws.views.sheetView[0].showGridLines = True
    ws.freeze_panes = "C9"

    # Fonts
    font_title = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    font_subtitle = Font(name="Calibri", size=9.5, italic=True, color="1E293B")
    font_sec_hdr = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    font_col_hdr = Font(name="Calibri", size=9.5, bold=True, color="FFFFFF")
    font_data = Font(name="Calibri", size=9.5, color="0F172A")
    font_data_bold = Font(name="Calibri", size=9.5, bold=True, color="0F172A")
    font_muted = Font(name="Calibri", size=8.5, color="64748B")

    # Borders
    border_light = Side(border_style="thin", color="CBD5E1")
    border_dark = Side(border_style="medium", color="64748B")
    cell_border = Border(left=border_light, right=border_light, top=border_light, bottom=border_light)
    header_border = Border(left=border_light, right=border_light, top=border_light, bottom=border_dark)

    # Title Banner
    ws.merge_cells("A1:N1")
    ws["A1"] = "AGENCY RECRUITER DIRECTORY & IDENTIFICATION ROSTER"
    ws["A1"].font = font_title
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws["A1"].fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    ws.row_dimensions[1].height = 34

    # Subtitle
    ws.merge_cells("A2:N2")
    ws["A2"] = "Official Recruiter IDs, Agent Codes, Contact Details, License Credentials & Performance Metrics"
    ws["A2"].font = font_subtitle
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws["A2"].fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    ws.row_dimensions[2].height = 20

    ws.row_dimensions[3].height = 8

    # Helper for KPI cards
    def style_kpi(start_col, end_col, bg, border_col, txt_col, label, val_formula, sub_txt):
        side = Side(border_style="thin", color=border_col)
        bdr = Border(left=side, right=side, top=side, bottom=side)
        fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")

        ws.merge_cells(f"{start_col}4:{end_col}4")
        ws.merge_cells(f"{start_col}5:{end_col}5")
        ws.merge_cells(f"{start_col}6:{end_col}6")

        ws[f"{start_col}4"] = label
        ws[f"{start_col}4"].font = Font(name="Calibri", size=9, bold=True, color=txt_col)
        ws[f"{start_col}4"].alignment = Alignment(horizontal="center", vertical="center")

        ws[f"{start_col}5"] = val_formula
        ws[f"{start_col}5"].font = Font(name="Calibri", size=18, bold=True, color=txt_col)
        ws[f"{start_col}5"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"{start_col}5"].number_format = "#,##0"

        ws[f"{start_col}6"] = sub_txt
        ws[f"{start_col}6"].font = Font(name="Calibri", size=8.5, color=txt_col)
        ws[f"{start_col}6"].alignment = Alignment(horizontal="center", vertical="center")

        from openpyxl.utils.cell import range_boundaries
        for r in range(4, 7):
            min_c, _, max_c, _ = range_boundaries(f"{start_col}{r}:{end_col}{r}")
            for c in range(min_c, max_c + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = fill
                cell.border = bdr

    style_kpi("B", "D", "EBF4FF", "93C5FD", "1E40AF", "TOTAL RECRUITERS", '=COUNTA(A9:A35)', "Authorized agency recruiters")
    style_kpi("E", "G", "DCFCE7", "86EFAC", "15803D", "ACTIVE STATUS", '=COUNTIF(H9:H35, "Active")', "Currently sourcing talent")
    style_kpi("H", "J", "FEF3C7", "FCD34D", "B45309", "TOTAL SOURCED", '=SUM(J9:J35)', "Total candidates invited")
    style_kpi("K", "M", "E0F2FE", "7DD3FC", "0369A1", "ADD ATTENDED", '=SUM(K9:K35)', "Candidates attended ADD")

    ws.row_dimensions[4].height = 16
    ws.row_dimensions[5].height = 26
    ws.row_dimensions[6].height = 16
    ws.row_dimensions[7].height = 8

    # Table Column Headers (Row 8)
    headers = [
        ("A", "Recruiter ID / Code", "center", 18),
        ("B", "Recruiter Full Name", "left", 24),
        ("C", "Email Address", "left", 26),
        ("D", "Contact Number", "center", 18),
        ("E", "Agency Unit / Team", "left", 20),
        ("F", "License / IC Code", "center", 18),
        ("G", "Gov ID / Verification", "left", 22),
        ("H", "Status", "center", 14),
        ("I", "Date Added", "center", 14),
        ("J", "Recruits Sourced", "center", 16),
        ("K", "Attended ADD", "center", 14),
        ("L", "LMS In Progress", "center", 15),
        ("M", "LMS Completed", "center", 15),
        ("N", "ID File Reference / Upload Status", "left", 30),
    ]

    for col, title, align, width in headers:
        cell = ws[f"{col}8"]
        cell.value = title
        cell.font = font_col_hdr
        cell.fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
        cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True)
        cell.border = header_border
        ws.column_dimensions[col].width = width

    ws.row_dimensions[8].height = 28

    # Initial Recruiter Records
    recruiters_data = [
        ("AGT-001", "Cedric", "cedric.axa1@gmail.com", "0917 888 9999", "Executive Agency Unit", "LIC-2024-001", "PRC Professional License", "Active", "2024-01-15", "Verified / Primary Recruiter"),
        ("AGT-002", "Sarah Jenkins (UM)", "sarah.jenkins@agency.com", "0918 222 3333", "Alpha Leaders Unit", "LIC-2023-088", "Unified Multi-Purpose ID", "Active", "2023-06-01", "Verified / Unit Manager"),
        ("AGT-003", "David Tan", "david.tan@agency.com", "0919 444 5555", "Apex Financial Team", "LIC-2024-112", "Passport / Driver's License", "Active", "2024-02-10", "Verified / Agency Leader"),
        ("AGT-004", "Elena Gomez", "elena.gomez@agency.com", "0920 666 7777", "Summit Advisors Unit", "LIC-2024-190", "PRC License ID", "Active", "2024-03-01", "Verified / Unit Leader"),
    ]

    for idx, rec in enumerate(recruiters_data, start=9):
        code, name, email, phone, unit, lic, gov_id, status, dt, id_ref = rec
        bg = "FFFFFF" if idx % 2 == 1 else "F8FAFC"
        row_fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")

        ws[f"A{idx}"] = code
        ws[f"B{idx}"] = name
        ws[f"C{idx}"] = email
        ws[f"D{idx}"] = phone
        ws[f"E{idx}"] = unit
        ws[f"F{idx}"] = lic
        ws[f"G{idx}"] = gov_id
        ws[f"H{idx}"] = status
        ws[f"I{idx}"] = dt
        ws[f"J{idx}"] = f'=COUNTIF(\'Recruit Monitoring Tracker\'!$E$9:$E$65, "*{name}*")'
        ws[f"K{idx}"] = f'=COUNTIFS(\'Recruit Monitoring Tracker\'!$E$9:$E$65, "*{name}*", \'Recruit Monitoring Tracker\'!$H$9:$H$65, "Yes")'
        ws[f"L{idx}"] = f'=COUNTIFS(\'Recruit Monitoring Tracker\'!$E$9:$E$65, "*{name}*", \'Recruit Monitoring Tracker\'!$L$9:$L$65, "In Progress")'
        ws[f"M{idx}"] = f'=COUNTIFS(\'Recruit Monitoring Tracker\'!$E$9:$E$65, "*{name}*", \'Recruit Monitoring Tracker\'!$L$9:$L$65, "Yes")'
        ws[f"N{idx}"] = id_ref

        for col, _, align, _ in headers:
            cell = ws[f"{col}{idx}"]
            cell.font = font_data_bold if col in ["A", "B", "J", "K"] else font_data
            cell.alignment = Alignment(horizontal=align, vertical="center")
            cell.border = cell_border
            cell.fill = row_fill
            if col in ["J", "K", "L", "M"]:
                cell.number_format = "#,##0"

        ws.row_dimensions[idx].height = 22

    # Blank template rows for new uploaded recruiters
    for idx in range(13, 36):
        bg = "FFFFFF" if idx % 2 == 1 else "F8FAFC"
        row_fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")

        ws[f"A{idx}"] = f"AGT-{idx-8:03d}"
        ws[f"B{idx}"] = ""
        ws[f"C{idx}"] = ""
        ws[f"D{idx}"] = ""
        ws[f"E{idx}"] = ""
        ws[f"F{idx}"] = ""
        ws[f"G{idx}"] = ""
        ws[f"H{idx}"] = "Active"
        ws[f"I{idx}"] = ""
        ws[f"J{idx}"] = f'=IF(B{idx}="","",COUNTIF(\'Recruit Monitoring Tracker\'!$E$9:$E$65, "*"&B{idx}&"*"))'
        ws[f"K{idx}"] = f'=IF(B{idx}="","",COUNTIFS(\'Recruit Monitoring Tracker\'!$E$9:$E$65, "*"&B{idx}&"*", \'Recruit Monitoring Tracker\'!$H$9:$H$65, "Yes"))'
        ws[f"L{idx}"] = f'=IF(B{idx}="","",COUNTIFS(\'Recruit Monitoring Tracker\'!$E$9:$E$65, "*"&B{idx}&"*", \'Recruit Monitoring Tracker\'!$L$9:$L$65, "In Progress"))'
        ws[f"M{idx}"] = f'=IF(B{idx}="","",COUNTIFS(\'Recruit Monitoring Tracker\'!$E$9:$E$65, "*"&B{idx}&"*", \'Recruit Monitoring Tracker\'!$L$9:$L$65, "Yes"))'
        ws[f"N{idx}"] = ""

        for col, _, align, _ in headers:
            cell = ws[f"{col}{idx}"]
            cell.font = font_data_bold if col in ["A", "B", "J", "K"] else font_data
            cell.alignment = Alignment(horizontal=align, vertical="center")
            cell.border = cell_border
            cell.fill = row_fill
            if col in ["J", "K", "L", "M"]:
                cell.number_format = "#,##0"

        ws.row_dimensions[idx].height = 20

    # Data Validation for Status
    dv_status = DataValidation(type="list", formula1='"Active,Inactive,On Leave,Pending Verification"', allow_blank=True)
    ws.add_data_validation(dv_status)
    dv_status.add("H9:H35")
