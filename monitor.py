import os
import requests
from bs4 import BeautifulSoup
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# URL to monitor
url = "https://www.stwdo.de/wohnen/aktuelle-wohnangebote"

# Email details
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "mishrasiddhant911@gmail.com"  # Replace with your sender email
recipient_email = "mishrasiddhant911@gmail.com"  # Replace with your recipient email
sender_password = os.getenv("EMAIL_PASSWORD")  # Fetch the password from GitHub Secrets

# File to store the previous hash
hash_file = "hash.txt"

def send_email_notification():
    """
    Sends an email notification when a change is detected.
    """
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

def get_current_hash():
    """
    Fetches the website content and returns its hash.
    """
    try:
        print("Fetching website content...")
        response = requests.get(url, timeout=10)  # Set timeout to avoid hanging
        soup = BeautifulSoup(response.content, "html.parser")
        current_content = soup.get_text()  # Extract text content
        current_hash = hashlib.md5(current_content.encode("utf-8")).hexdigest()
        print("✅ Website content fetched and hashed.")
        return current_hash
    except Exception as e:
        print(f"❌ Failed to fetch website content: {e}")
        return None

def load_previous_hash():
    """
    Loads the previous hash from the hash file, if it exists.
    """
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            return f.read().strip()
    return ""

def save_current_hash(current_hash):
    """
    Saves the current hash to the hash file.
    """
    with open(hash_file, "w") as f:
        f.write(current_hash)

def main():
    """
    Main function to check for changes and send notifications if necessary.
    """
    # Load the previous hash
    previous_hash = load_previous_hash()

    # Get the current hash
    current_hash = get_current_hash()
    if current_hash is None:
        print("❌ Skipping check due to error fetching website.")
        return

    # Compare hashes and send email if changed
    if previous_hash and current_hash != previous_hash:
        print("🚨 Change detected! Sending notification...")
        send_email_notification()
    else:
        print("✅ No changes detected.")

    # Save the current hash for future comparisons
    save_current_hash(current_hash)
    print("✅ Monitoring check completed.")

# Run the main function
if __name__ == "__main__":
    main()
