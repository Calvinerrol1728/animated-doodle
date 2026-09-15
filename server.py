import http.server
import socketserver
import json
import os
import urllib.parse
import openpyxl

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_recruits_data():
    wb = openpyxl.load_workbook(os.path.join(DIRECTORY, "Recruit_Monitoring_Tracker.xlsx"), data_only=True)
    ws1 = wb["Recruit Monitoring Tracker"]
    recruits = []
    for r in range(9, 24):
        recruits.append({
            "id": ws1[f"A{r}"].value,
            "name": ws1[f"B{r}"].value,
            "phone": ws1[f"C{r}"].value,
            "email": ws1[f"D{r}"].value,
            "recruiter": ws1[f"E{r}"].value,
            "sourced_date": str(ws1[f"F{r}"].value)[:10] if ws1[f"F{r}"].value else "",
            "add_sched": str(ws1[f"G{r}"].value)[:10] if ws1[f"G{r}"].value else "",
            "attended_add": ws1[f"H{r}"].value,
            "add_date": str(ws1[f"I{r}"].value)[:10] if ws1[f"I{r}"].value else "-",
            "add_remarks": ws1[f"J{r}"].value or "",
            "lms_date": str(ws1[f"K{r}"].value)[:10] if ws1[f"K{r}"].value else "-",
            "completed_lms": ws1[f"L{r}"].value,
            "lms_comp_date": str(ws1[f"M{r}"].value)[:10] if ws1[f"M{r}"].value else "-",
            "progress": f"{int((ws1[f'N{r}'].value or 0) * 100)}%",
            "cert": ws1[f"O{r}"].value or "",
            "stage": ws1[f"P{r}"].value or "",
            "next_action": ws1[f"Q{r}"].value or "",
            "follow_up": str(ws1[f"R{r}"].value)[:10] if ws1[f"R{r}"].value else "-",
            "notes": ws1[f"S{r}"].value or ""
        })
    return recruits

class CustomHandler(http.server.SimpleHTTPRequestHandler):
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
        # Default file serving (index.html, etc.)
        super().do_GET()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
        print(f"Server started on http://0.0.0.0:{PORT}")
        httpd.serve_forever()
