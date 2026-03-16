import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "emmanuelshugadan@gmail.com"
SENDER_APP_PASSWORD = "zattmchvramyebzn"
RECEIVER_EMAIL = "emmanuelshugadan@gmail.com"

print("Starting email test...")
print(f"Sending from: {SENDER_EMAIL}")

try:
    print("Connecting to Gmail...")
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "Network Auditor Test"
    msg.attach(MIMEText("This is a test email from your Network Auditor!", "plain"))

    print("Logging in...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
        server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        print("Logged in! Sending...")
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

    print("SUCCESS — Email sent! Check your inbox.")

except smtplib.SMTPAuthenticationError:
    print("FAILED — Authentication error. Check your email and app password.")
except smtplib.SMTPException as e:
    print(f"FAILED — SMTP error: {e}")
except Exception as e:
    print(f"FAILED — Unexpected error: {e}")
