# email_notifications.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(user_email, flight_results):
    """
    Sends flight results to the user's email.
    
    :param user_email: Email address of the recipient.
    :param flight_results: Flight results to include in the email.
    """
    sender_email = "sagarbmw1@gmail.com"
    sender_password = "jnqd bhdz gbbd xsoa"  # Use Gmail App Password here, not your regular Gmail password
    
    subject = "Your Flight Results"
    
    # Creating the body of the email (HTML formatted)
    body = f"""
    <html>
    <body>
        <p>Dear User,</p>
        <p>Here are your flight results:</p>
        <pre>{flight_results}</pre>  <!-- Flight results in plain text format -->
        <p>Best regards,<br>Your Flight Finder Team</p>
    </body>
    </html>
    """

    # Create the email message with multipart
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    
    # Attach the body with HTML content
    message.attach(MIMEText(body, "html"))  # Note the 'html' MIME type

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Log in with App Password
            server.sendmail(sender_email, user_email, message.as_string())  # Send email
        
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
