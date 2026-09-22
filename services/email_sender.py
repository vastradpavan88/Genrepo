import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_email(recipient_email, pdf_path):

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if sender_email:
        sender_email = sender_email.strip()

    if sender_password:
        sender_password = sender_password.replace(" ", "").strip()

    if recipient_email:
        recipient_email = recipient_email.strip()

    if not sender_email:
        raise ValueError(
            "EMAIL_ADDRESS is missing in .env file."
        )

    if not sender_password:
        raise ValueError(
            "EMAIL_PASSWORD is missing in .env file."
        )

    if not recipient_email:
        raise ValueError(
            "Recipient email is missing from Excel."
        )

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    message = EmailMessage()

    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Automated Email Report"

    message.set_content(
        "Hello,\n\n"
        "Please find the automated report attached.\n\n"
        "This report was generated automatically "
        "from the uploaded Excel file.\n\n"
        "Regards,\n"
        "Automated Email Report Generator"
    )

    with open(pdf_path, "rb") as pdf_file:
        message.add_attachment(
            pdf_file.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(pdf_path)
        )

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=30
        ) as smtp:

            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(
                sender_email,
                sender_password
            )

            smtp.send_message(message)

    except smtplib.SMTPAuthenticationError:

        raise ValueError(
            "Gmail authentication failed. "
            "Check EMAIL_ADDRESS and Google App Password."
        )

    except smtplib.SMTPException as error:

        raise ValueError(
            f"Gmail SMTP error: {error}"
        )

    except OSError as error:

        raise ValueError(
            f"Gmail connection error: {error}"
        )

    print(
        f"Email successfully sent to {recipient_email}"
    )

    return True