import time
import json
import requests
from datetime import datetime
from alerts import send_email_alert, send_telegram_alert
from dotenv import load_dotenv
import os

load_dotenv()

with open("config.json") as f:
    config = json.load(f)
    URLS_TO_MONITOR = config["urls"]
    CHECK_INTERVAL = config.get("interval", 60)

def check_website(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error Checking {url}: {e}")
        return False

def log_status(url, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] {url} - {'UP' if status else 'DOWN'}\n"
    with open("logs/monitor.log", "a") as f:
        f.write(log_line)
    return log_line

if __name__ == "__main__":
    print("✅ Web Monitor Started")
    while True:
        for url in URLS_TO_MONITOR:
            is_up = check_website(url)
            log = log_status(url, is_up)
            print(log.strip())
            if not is_up:
                alert_message = f"🚨 Website DOWN: {url}"
                send_email_alert("Website Down Alert", alert_message)
                send_telegram_alert(alert_message)
        time.sleep(CHECK_INTERVAL)
