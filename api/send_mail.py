import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()


email = os.getenv("YOUR_EMAIL_ENV_VAR")
password = os.getenv("YOUR_PASSWORD_ENV_VAR")


def send_email(to_email, subject, content):
 
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = email  # replace with your email
    msg['To'] = to_email

    print(to_email, subject, content)


    # Use Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Upgrade the connection to secure encrypted SSL
    server.login(email, password)
    server.send_message(msg)
    server.quit()


def add_exam_request(exam_name):
    print("email is send")
    try:
        send_email(
        to_email=email,
        subject='New Exam Request Reminder',
        content=f"{exam_name}  has been requested.Please review and add if applicable."
     
    )
        
        
    
    
    except Exception as e:
        print(f"Error sending email: {str(e)}")



