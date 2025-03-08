import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body):
    """
    Sends an email to the specified recipient.

    Args:
        to (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body content of the email.
    """
    sender = "your_email@gmail.com"
    password = "your_email_password"

    # Create the email message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender, password)
            server.sendmail(sender, to, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_notification(to, subject, body):
    """
    Sends an email notification.

    Args:
        to (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body content of the email.
    """
    send_email(to, subject, body)

# Example usage
if __name__ == "__main__":
    send_notification(
        to="recipient_email@example.com",
        subject="Test Notification",
        body="This is a test email notification."
    )