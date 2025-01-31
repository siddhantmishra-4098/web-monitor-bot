import os  # Import for reading environment variables
import requests
from bs4 import BeautifulSoup
import hashlib
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# URL to monitor
url = "https://www.stwdo.de/wohnen/aktuelle-wohnangebote"

# Email details
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "mishrasiddhant911@gmail.com"  # Replace with your email
recipient_email = "mishrasiddhant911@gmail.com"  # Replace with recipient email

# Get the email password from GitHub Secrets
sender_password = os.getenv("EMAIL_PASSWORD")  # Fetches the secret value

def send_email_notification():
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Change Detected on Website"
        body = f"A change was detected on {url} at {time.ctime()}."
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("✅ Email notification sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Initial hash
previous_hash = ""

while True:
    try:
        # Get page content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        current_content = soup.get_text()  # Extract text content

        # Create a hash of the content
        current_hash = hashlib.md5(current_content.encode("utf-8")).hexdigest()

        # Compare hashes
        if previous_hash and current_hash != previous_hash:
            print("🚨 Change detected!")
            send_email_notification()

        previous_hash = current_hash

        # Wait 10 minutes before checking again
        time.sleep(300)

    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(30)
