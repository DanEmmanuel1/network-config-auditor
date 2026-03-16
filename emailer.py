import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rich.console import Console

console = Console()

# ============================================================
# FILL THESE IN WITH YOUR DETAILS
SENDER_EMAIL = "emmanuelshugadan@gmail.com"
SENDER_APP_PASSWORD = "zattmchvramyebzn"
RECEIVER_EMAIL = "emmanuelshugadan@gmail.com"
# ============================================================

def send_alert(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        console.print("[green]✔ Alert email sent successfully[/green]")

    except Exception as e:
        console.print(f"[red]✘ Failed to send email: {e}[/red]")

def build_alert_body(findings):
    lines = []
    lines.append("=" * 50)
    lines.append("NETWORK AUDITOR — SECURITY ALERT")
    lines.append("=" * 50)
    lines.append("")

    for category, items in findings.items():
        if items:
            lines.append(f"[{category}]")
            for item in items:
                lines.append(f"  ⚠ {item}")
            lines.append("")

    lines.append("=" * 50)
    lines.append("Run your auditor for full details.")
    lines.append("=" * 50)
    return "\n".join(lines)