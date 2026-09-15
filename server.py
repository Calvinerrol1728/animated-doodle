import http.server
import socketserver
import json
import os
import urllib.parse
import openpyxl
import datetime
import csv
import email_service

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_recruits_data():
    wb = openpyxl.load_workbook(os.path.join(DIRECTORY, "Recruit_Monitoring_Tracker.xlsx"), data_only=True)
    ws1 = wb["Recruit Monitoring Tracker"]
    recruits = []
    for r in range(9, 66):
        name = ws1[f"B{r}"].value
        if not name or not str(name).strip():
            continue
        
        attended = ws1[f"H{r}"].value
        lms = ws1[f"L{r}"].value
        stage = ws1[f"P{r}"].value or ""
        if not stage:
            if lms == "Yes":
                stage = "LMS Completed (Ready for Exam)"
            elif lms == "In Progress":
                stage = "LMS In Progress"
            elif attended == "Yes":
                stage = "ADD Attended - Awaiting LMS"
            elif attended == "Rescheduled":
                stage = "ADD Rescheduled"
            elif attended == "Pending":
                stage = "ADD Scheduled"
            elif attended == "No":
                stage = "ADD Missed - Follow Up"
            else:
                stage = "Initial Prospect"

        recruits.append({
            "id": ws1[f"A{r}"].value or f"REC-{r-8:03d}",
            "name": name,
            "phone": ws1[f"C{r}"].value or "-",
            "email": ws1[f"D{r}"].value or "-",
            "recruiter": ws1[f"E{r}"].value or "Cedric (cedric.axa1@gmail.com)",
            "sourced_date": str(ws1[f"F{r}"].value)[:10] if ws1[f"F{r}"].value else "",
            "add_sched": str(ws1[f"G{r}"].value)[:10] if ws1[f"G{r}"].value else "",
            "attended_add": ws1[f"H{r}"].value or "-",
            "add_date": str(ws1[f"I{r}"].value)[:10] if ws1[f"I{r}"].value else "-",
            "add_remarks": ws1[f"J{r}"].value or "",
            "lms_date": str(ws1[f"K{r}"].value)[:10] if ws1[f"K{r}"].value else "-",
            "completed_lms": ws1[f"L{r}"].value or "Not Started",
            "lms_comp_date": str(ws1[f"M{r}"].value)[:10] if ws1[f"M{r}"].value else "-",
            "progress": f"{int((ws1[f'N{r}'].value or 0) * 100)}%" if ws1[f"N{r}"].value is not None else "0%",
            "cert": ws1[f"O{r}"].value or "",
            "stage": stage,
            "next_action": ws1[f"Q{r}"].value or "",
            "follow_up": str(ws1[f"R{r}"].value)[:10] if ws1[f"R{r}"].value else "-",
            "notes": ws1[f"S{r}"].value or ""
        })
    return recruits

def register_recruit_to_excel(data):
    excel_path = os.path.join(DIRECTORY, "Recruit_Monitoring_Tracker.xlsx")
    wb = openpyxl.load_workbook(excel_path)
    ws1 = wb["Recruit Monitoring Tracker"]
    
    # Find next available row
    next_row = None
    for r in range(9, 100):
        val = ws1[f"B{r}"].value
        if not val or not str(val).strip():
            next_row = r
            break
    if not next_row:
        next_row = 66

    recruit_id = f"REC-{next_row-8:03d}"
    full_name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    recruiter = data.get("recruiter", "").strip() or "Cedric (cedric.axa1@gmail.com)"
    add_date_str = data.get("add_date", "").strip()
    occupation = data.get("occupation", "").strip()
    interest = data.get("interest", "").strip()
    questions = data.get("questions", "").strip()

    today = datetime.date(2026, 9, 15)
    try:
        add_date = datetime.datetime.strptime(add_date_str, "%Y-%m-%d").date()
    except Exception:
        add_date = datetime.date(2026, 9, 19)

    # Check if date attended
    if add_date < today:
        attended_status = "Yes"
        attended_date = add_date
        next_action = "Follow up on ADD feedback & check readiness to process LMS"
    else:
        attended_status = "Pending"
        attended_date = None
        next_action = "Send ADD confirmation SMS & Zoom/venue details"

    ws1[f"A{next_row}"] = recruit_id
    ws1[f"B{next_row}"] = full_name
    ws1[f"C{next_row}"] = phone
    ws1[f"D{next_row}"] = email
    ws1[f"E{next_row}"] = recruiter
    ws1[f"F{next_row}"] = today
    ws1[f"G{next_row}"] = add_date
    ws1[f"H{next_row}"] = attended_status
    ws1[f"I{next_row}"] = attended_date
    ws1[f"J{next_row}"] = f"Registered via ADD Online Form. Field: {occupation}. Goal: {interest}."
    ws1[f"K{next_row}"] = None
    ws1[f"L{next_row}"] = "Not Started"
    ws1[f"M{next_row}"] = None
    ws1[f"N{next_row}"] = 0.0
    ws1[f"O{next_row}"] = "Pending ADD session"
    ws1[f"P{next_row}"] = f'=IF(B{next_row}="","",IF(L{next_row}="Yes","LMS Completed (Ready for Exam)",IF(L{next_row}="In Progress","LMS In Progress",IF(H{next_row}="Yes","ADD Attended - Awaiting LMS",IF(H{next_row}="Rescheduled","ADD Rescheduled",IF(H{next_row}="Pending","ADD Scheduled",IF(H{next_row}="No","ADD Missed - Follow Up","Initial Prospect")))))))'
    ws1[f"Q{next_row}"] = next_action
    ws1[f"R{next_row}"] = add_date if attended_status == "Pending" else today + datetime.timedelta(days=1)
    notes_part = f" Note: {questions}." if questions else ""
    ws1[f"S{next_row}"] = f"Online registration for ADD on {add_date}. Thank-you email sent from cedric.axa1@gmail.com.{notes_part}"

    # Formats
    for col_l in ["F", "G", "I", "K", "M", "R"]:
        ws1[f"{col_l}{next_row}"].number_format = "yyyy-mm-dd"
    ws1[f"N{next_row}"].number_format = "0.0%"

    wb.save(excel_path)

    # Send / log thank-you email from cedric.axa1@gmail.com
    email_result = email_service.send_thank_you_email(full_name, email, recruit_id, str(add_date))

    # Append to CSV export
    try:
        csv_path = os.path.join(DIRECTORY, "Recruit_Monitoring_Export.csv")
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                recruit_id,
                full_name,
                phone,
                email,
                recruiter,
                str(today),
                str(add_date),
                attended_status,
                str(attended_date or ""),
                ws1[f"J{next_row}"].value,
                "",
                "Not Started",
                "",
                0,
                "Pending ADD session",
                "",
                next_action,
                str(ws1[f"R{next_row}"].value or ""),
                ws1[f"S{next_row}"].value
            ])
    except Exception as e:
        print(f"Error updating CSV: {e}")

    return recruit_id, email_result

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/recruits":
            data = get_recruits_data()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return
        elif parsed.path == "/register":
            register_path = os.path.join(DIRECTORY, "register.html")
            if os.path.exists(register_path):
                with open(register_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
        elif parsed.path in ["/download-form", "/ADD_Registration_Form.html"]:
            register_path = os.path.join(DIRECTORY, "register.html")
            if os.path.exists(register_path):
                with open(register_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="ADD_Registration_Form.html"')
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
        elif parsed.path.startswith("/outbox/"):
            filename = os.path.basename(parsed.path)
            file_path = os.path.join(DIRECTORY, "outbox", filename)
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
        elif parsed.path in ["/download", "/Recruit_Monitoring_Tracker.xlsx"]:
            filepath = os.path.join(DIRECTORY, "Recruit_Monitoring_Tracker.xlsx")
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                self.send_header("Content-Disposition", 'attachment; filename="Recruit_Monitoring_Tracker.xlsx"')
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
        # Default static file serving
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/register":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len)
            try:
                data = json.loads(post_body.decode("utf-8"))
            except Exception:
                parsed_dict = urllib.parse.parse_qs(post_body.decode("utf-8"))
                data = {k: v[0] for k, v in parsed_dict.items()}

            if not data.get("name"):
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Candidate name is required."}).encode("utf-8"))
                return

            try:
                new_id, email_res = register_recruit_to_excel(data)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "recruit_id": new_id,
                    "message": f"Successfully registered {data.get('name')}! Assigned ID: {new_id}.",
                    "email": email_res
                }).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
        print(f"Server started on http://0.0.0.0:{PORT}")
        httpd.serve_forever()
