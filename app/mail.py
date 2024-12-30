import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_code_mail():
    sender_email = "saastest74@gmail.com"
    receiver_email = "hermannnzeudeu@gmail.com"
    password = "flxw jjeo rrfx jury"

    # Créer le message
    subject = "Sujet de l'email"
    body = "Ceci est le contenu de l'email."

    # Construire l'email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Ajouter le corps de l'email
    message.attach(MIMEText(body, "plain"))

    # Envoyer l'email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Sécuriser la connexion
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email envoyé avec succès!")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")