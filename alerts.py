import smtplib
import os
import requests
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email_alert(subject, message):
    try:
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = email_user
        msg["To"] = email_user

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)

        print("✅ Email sent")
    except Exception as e:
        print(f"❌ Email alert failed: {e}")

def send_telegram_alert(message):
    bot_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("✅ Telegram alert sent")
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")
