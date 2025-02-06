import logging
import random
from app.models.user import User, OneTimePasscode
from typing import List

from app.config import settings

from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

# Configuration du logger
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


sender_email = settings.sender_email
password = settings.password
smtp_server = settings.smtp_server
server_port = settings.server_port

class EmailBody(BaseModel):
    to: str
    subject: str
    message: str

class EmailSchema(BaseModel):
    email: EmailStr


def send_normal_mail(email: EmailSchema, subject: str, email_body: str) -> JSONResponse:
    """
    Author: hermannnzeudeu@gmail.com
    Description: send normal mail
    """

    # Configurer les paramètres de l'email
    receiver_email = email

    # Créer le message
    subject = "Sujet de l'email"
    body = email_body

    # Construire l'email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Ajouter le corps de l'email
    message.attach(MIMEText(body, "html"))

    # Envoyer l'email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Sécuriser la connexion
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email envoyé avec succès!")
    except Exception as e:
        print(sender_email)
        print(password == "fogu mmfp ybcx znbp")
        print(password)
        print(f"Une erreur est survenue : {e}")

    
def generateOtp(): 
    """
    Author: hermannnzeudeu@gmail.com
    Description: generate otp code for verification
    """
    otp = ""
    for i in range(8):
        otp += str(random.randint(1,9))
    return otp

async def send_code_email(email: EmailSchema, db: Session) -> JSONResponse:
    """
    Author: hermannnzeudeu@gmail.com
    Description: send otp code to user
    """
    receiver_email = email
    subject = "one time code password for email verification"
    otp_code = generateOtp()
    user = db.query(User).filter(User.email == email).first()
    current_site = "Abraham.app"
    email_body = f"<h3>Hi {user.username},</h3> thanks for signing up on {current_site} please verify your email with the \n one time passcode <b>{otp_code}</b>"

    new_otp = OneTimePasscode(code=otp_code, owner_id=user.id)
    db.add(new_otp)
    db.commit()
    try:
        send_normal_mail(receiver_email, subject, email_body)
        return JSONResponse(content={"message": "Email sent successfully"})
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return JSONResponse(content={"message": "Error sending email"}, status_code=500) 
     