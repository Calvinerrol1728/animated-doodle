import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import datetime
import urllib.parse

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
OUTBOX_DIR = os.path.join(DIRECTORY, "outbox")
os.makedirs(OUTBOX_DIR, exist_ok=True)

SENDER_EMAIL = "cedric.axa1@gmail.com"
SENDER_NAME = "Cedric"

def generate_email_content(candidate_name, candidate_email, recruit_id, add_date):
    subject = f"Thank You for Registering for Agency Discovery Day (ADD)! | Cedric"

    text_body = f"""Dear {candidate_name},

Thank you for registering for our upcoming Agency Discovery Day (ADD)! I am delighted to welcome you to our career preview orientation.

Your registration has been successfully confirmed and recorded in our recruit monitoring tracker:
• Candidate Name: {candidate_name}
• Candidate ID: {recruit_id}
• Scheduled ADD Session: {add_date}
• Host / Recruiter: {SENDER_NAME} ({SENDER_EMAIL})

WHAT YOU WILL DISCOVER DURING THE AGENCY DISCOVERY DAY (ADD):
1. An inside look into the fulfilling and lucrative career of a Licensed Financial Advisor.
2. How to build your own business with flexible work-from-home/hybrid hours and unlimited income potential.
3. The step-by-step roadmap to obtaining your license, including access to our online Learning Management System (LMS) training modules.

WHAT HAPPENS NEXT:
I will send you the Zoom orientation link and session preparation details before our meeting. If you have any questions or schedule adjustments in the meantime, please feel free to reply directly to this email at {SENDER_EMAIL}.

I look forward to meeting you at our ADD session!

Warm regards,

{SENDER_NAME}
Financial Advisory Agency Leader
Email: {SENDER_EMAIL}
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Thank You for Registering for ADD</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; color: #1e293b; margin: 0; padding: 20px; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 14px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }}
    .header {{ background: linear-gradient(135deg, #1B365D 0%, #2563EB 100%); color: #ffffff; padding: 32px 24px; text-align: center; }}
    .header h1 {{ margin: 0 0 6px 0; font-size: 22px; font-weight: 800; letter-spacing: -0.01em; }}
    .header p {{ margin: 0; font-size: 13.5px; color: #bfdbfe; font-weight: 400; }}
    .content {{ padding: 28px 24px; font-size: 14px; line-height: 1.65; color: #334155; }}
    .greeting {{ font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 14px; }}
    .box {{ background: #eff6ff; border-left: 4px solid #2563eb; padding: 16px 18px; border-radius: 8px; margin: 20px 0; }}
    .box p {{ margin: 5px 0; font-size: 13.5px; }}
    .box strong {{ color: #1e3a8a; }}
    .points {{ margin: 18px 0; }}
    .point {{ margin-bottom: 10px; padding-left: 4px; }}
    .footer {{ background: #f8fafc; padding: 20px 24px; font-size: 12px; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; line-height: 1.5; }}
    .badge {{ display: inline-block; background: #dcfce7; color: #15803d; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 12px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Agency Discovery Day (ADD)</h1>
      <p>Career Preview Orientation Confirmation</p>
    </div>
    <div class="content">
      <div class="greeting">Dear {candidate_name},</div>
      <p>Thank you for registering for our upcoming <strong>Agency Discovery Day (ADD)</strong>! I am delighted to welcome you to our career preview session.</p>
      
      <div class="box">
        <p><strong>Candidate ID:</strong> {recruit_id} <span class="badge">Confirmed</span></p>
        <p><strong>Scheduled ADD Date:</strong> {add_date}</p>
        <p><strong>Host / Coordinator:</strong> {SENDER_NAME} (&lt;<a href="mailto:{SENDER_EMAIL}" style="color:#2563eb;">{SENDER_EMAIL}</a>&gt;)</p>
        <p><strong>Status:</strong> Successfully logged in Recruit Monitoring Tracker</p>
      </div>

      <p><strong>What You Will Discover During the Session:</strong></p>
      <div class="points">
        <div class="point">🔹 <strong>The Life of a Financial Advisor:</strong> How you can build a meaningful, client-centered professional practice.</div>
        <div class="point">🔹 <strong>Income & Flexibility:</strong> How our advisors manage their own schedules while achieving high financial rewards.</div>
        <div class="point">🔹 <strong>Licensing Roadmap:</strong> Clear guidance on beginning your online Learning Management System (LMS) modules.</div>
      </div>

      <p style="margin-top: 20px;">I will send you the Zoom webinar link and preparation guidelines before the orientation. If you have any questions or need to adjust your schedule, please reply directly to this email at <a href="mailto:{SENDER_EMAIL}" style="color:#2563eb; font-weight: 600;">{SENDER_EMAIL}</a>.</p>
      
      <p style="margin-top: 25px; margin-bottom: 4px;">Warm regards,</p>
      <p style="margin-top: 0;">
        <strong style="font-size: 15px; color: #0f172a;">{SENDER_NAME}</strong><br>
        <span style="font-size: 13px; color: #64748b;">Financial Advisory Agency Leader</span><br>
        <a href="mailto:{SENDER_EMAIL}" style="color: #2563eb; font-size: 13px; text-decoration: none;">{SENDER_EMAIL}</a>
      </p>
    </div>
    <div class="footer">
      Sent by {SENDER_NAME} ({SENDER_EMAIL}) for your Agency Discovery Day reservation.<br>
      Candidate ID: {recruit_id} | Date: {datetime.date.today()}
    </div>
  </div>
</body>
</html>
"""

    # Generate mailto link for pre-filled email client
    mailto_params = {
        "subject": subject,
        "body": text_body
    }
    mailto_url = f"mailto:{candidate_email}?{urllib.parse.urlencode(mailto_params)}"

    return {
        "sender": f"{SENDER_NAME} <{SENDER_EMAIL}>",
        "sender_email": SENDER_EMAIL,
        "recipient": candidate_email,
        "recipient_name": candidate_name,
        "subject": subject,
        "text": text_body,
        "html": html_body,
        "mailto": mailto_url
    }

def send_thank_you_email(candidate_name, candidate_email, recruit_id, add_date):
    """
    Sends thank-you email to recruit from cedric.axa1@gmail.com.
    If SMTP credentials are provided in env, dispatches over TLS.
    Also saves a rendered copy to outbox/ and logs to sent_emails.log.
    """
    email_data = generate_email_content(candidate_name, candidate_email, recruit_id, add_date)
    
    # Always save a rendered HTML copy in outbox for review/preview
    outbox_file = os.path.join(OUTBOX_DIR, f"{recruit_id}.html")
    with open(outbox_file, "w", encoding="utf-8") as f:
        f.write(email_data["html"])

    # Log to sent_emails.log
    log_file = os.path.join(DIRECTORY, "sent_emails.log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] FROM: {email_data['sender']} | TO: {candidate_email} | SUBJECT: {email_data['subject']} | ID: {recruit_id}\n")

    # Check for SMTP credentials in environment
    smtp_user = os.environ.get("SMTP_USER", SENDER_EMAIL)
    smtp_pass = os.environ.get("SMTP_PASS") or os.environ.get("GMAIL_APP_PASS")
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))

    delivery_status = "Dispatched & Logged (Outbox)"

    if smtp_pass:
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = email_data["sender"]
            msg["To"] = candidate_email
            msg["Reply-To"] = SENDER_EMAIL
            msg["Subject"] = email_data["subject"]

            msg.attach(MIMEText(email_data["text"], "plain"))
            msg.attach(MIMEText(email_data["html"], "html"))

            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(SENDER_EMAIL, [candidate_email], msg.as_string())
            
            delivery_status = "Delivered via Gmail SMTP"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] -> SMTP SUCCESS to {candidate_email}\n")
        except Exception as e:
            delivery_status = f"SMTP Logged (Error: {str(e)[:40]}...)"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] -> SMTP WARNING: {e}\n")

    return {
        "status": delivery_status,
        "from": SENDER_EMAIL,
        "to": candidate_email,
        "subject": email_data["subject"],
        "recruit_id": recruit_id,
        "outbox_path": f"/outbox/{recruit_id}.html",
        "mailto": email_data["mailto"]
    }

if __name__ == "__main__":
    result = send_thank_you_email("Maria Santos", "maria.santos@gmail.com", "REC-007", "2026-09-17")
    print("Test email processed:", result)
