import os
import requests
from bs4 import BeautifulSoup
import smtplib
from datetime import datetime

EMAIL = os.getenv("EMAIL_ADDRESS")
APP_PSW = os.getenv("APP_PSW")
SMTP_SERVER = os.getenv("SMTP_ADDRESS")
EMAIL_RECIPIENTS= os.getenv("EMAIL_RECIPIENTS").split(",")

URL = "https://www.cnyrate.com/cmb.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US"
}

TARGET_RATE = 520.94

response = requests.get(URL, headers=HEADERS, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

row = soup.find("tr", {"data-row-key": "CAD"})
if not row:
    raise ValueError("CAD row not found")

tds = row.find_all("td")
if len(tds) < 4:
    raise ValueError("Not enough columns in CAD row")

rate = round(float(tds[3].get_text(strip=True)), 2)
print(f"[{datetime.now()}] CAD rate:", rate)

if rate < TARGET_RATE:
    subject = "CAD Exchange Rate Alert!"
    body = f"CAD rate is now {rate}\n{URL}"

    email_content = f"""From: {EMAIL}
To: {", ".join(EMAIL_RECIPIENTS)}
Subject: {subject}

{body}
"""

    with smtplib.SMTP(SMTP_SERVER, 587) as connection:
        connection.starttls()
        connection.login(EMAIL, APP_PSW)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL_RECIPIENTS,
            msg=email_content.encode("utf-8")
        )

