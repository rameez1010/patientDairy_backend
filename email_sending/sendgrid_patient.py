from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config.env_config import settings


def sendgrid_email(to_emails: str, name: str, set_password_link: str):
    # Read the HTML content from the file
    with open("./email_sending/email_patient.html", "r") as file:
        html_content = file.read()

    html_content = html_content.replace("{{name}}", name)
    html_content = html_content.replace("{{url}}", set_password_link)

    

    message = Mail(
        from_email="info@biokrystal.com",
        to_emails=to_emails,
        subject="Welcome to BioKrystal",
        html_content=html_content,
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(str(e))


def send_patient_password_reset_email(to_email: str, name: str, reset_link: str):
    # Read the HTML content from the file
    with open("./email_sending/patient_reset_password_email.html", "r") as file:
        html_content = file.read()

    # Replace placeholders with actual values
    html_content = html_content.replace("{{name}}", name)
    html_content = html_content.replace("{{reset_link}}", reset_link)

    message = Mail(
        from_email="info@biokrystal.com",
        to_emails=to_email,
        subject="Reset Your BioKrystal Password",
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Patient password reset email sent to {to_email}, status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending patient password reset email: {str(e)}")
        return False

def send_patient_set_password_email(to_email: str, set_password_link: str):
    # Read the HTML content from the file
    with open("./email_sending/patient_set_password_email.html", "r") as file:
        html_content = file.read()

    # Replace placeholders with actual values
    html_content = html_content.replace("{{set_password_link}}", set_password_link)

    message = Mail(
        from_email="info@biokrystal.com",
        to_emails=to_email,
        subject="Set Your BioKrystal Password",
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Patient password reset email sent to {to_email}, status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending patient password reset email: {str(e)}")
        return False

def send_patient_otp_email(to_email: str, name: str, otp_code: str):
    # Read the HTML content from the file
    with open("./email_sending/patient_otp_email.html", "r") as file:
        html_content = file.read()

    # Replace placeholders with actual values
    html_content = html_content.replace("{{name}}", name)
    html_content = html_content.replace("{{otp_code}}", otp_code)

    message = Mail(
        from_email="info@biokrystal.com",
        to_emails=to_email,
        subject="Your BioKrystal Login Verification Code",
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Patient OTP email sent to {to_email}, status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending patient OTP email: {str(e)}")
        return False
