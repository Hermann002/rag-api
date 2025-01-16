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
    email: List[EmailStr]


async def send_normal_mail(email: EmailSchema, subject: str, email_body: str) -> JSONResponse:
    """
    Author: hermannnzeudeu@gmail.com
    Description: send normal mail
    """
    if isinstance(email, str):
        email_str = email
    else:
        email_str = email.email
    current_site = "Abraham.app"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email_str
    message["Subject"] = subject

    message.attach(MIMEText(email_body, "html"))
    try:
        with smtplib.SMTP(smtp_server, server_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, email_str, message.as_string())
            print("Email envoyé avec succès!")
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return JSONResponse(status_code=500, content={"message": "Internal server Error"})

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
    if isinstance(email, str):
        email_str = email
    else:
        email_str = email.email
    subject = "one time code password for email verification"
    otp_code = generateOtp()
    user = db.query(User).filter(User.email == email).first()
    current_site = "Abraham.app"
    email_body = f"<h3>Hi {user.username},</h3> thanks for signing up on {current_site} please verify your email with the \n one time passcode <b>{otp_code}</b>"

    new_otp = OneTimePasscode(code=otp_code, owner_id=user.id)
    db.add(new_otp)
    db.commit()

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email_str
    message["Subject"] = subject

    message.attach(MIMEText(email_body, "html"))
    try:
        with smtplib.SMTP(smtp_server, server_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, email_str, message.as_string())
            print("Email envoyé avec succès!")
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return JSONResponse(status_code=500, content={"message": "Internal server Error"})
     