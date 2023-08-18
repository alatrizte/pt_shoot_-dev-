import string, random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

def send_(mail, user):
    # Genera una key aleatoria para el nuevo usuario
    # Esta llave se envia por mail para confirmar su registro.
    key = ''
    for x in range(8):
        key += random.choice(string.ascii_letters + string.digits)

    # Cargar las variables de entorno
    load_dotenv()

    email_subject = "Codigo de verificación de Planning the Shoot" 
    sender_email_address = os.getenv("MAIL_USER") 
    receiver_email_address = mail 
    email_smtp = os.getenv("MAIL_HOST")
    email_password = os.getenv("MAIL_PASSWORD") 

    # Create an email message object 
    message = EmailMessage() 

    # Configure email headers 
    message['Subject'] = email_subject 
    message['From'] = sender_email_address 
    message['To'] = receiver_email_address 

    # Set email body text 
    message.set_content(f"Hola {user},<br>Para terminar su registro introduzca la clave:<h3>{key}</h3>", subtype='html') 

    # Set smtp server and port 
    server = smtplib.SMTP(email_smtp, '25') 

    # Identify this client to the SMTP server 
    server.ehlo() 

    # Secure the SMTP connection 
    # server.starttls() 

    # Login to email account 
    server.login(sender_email_address, email_password) 

    # Send email 
    server.send_message(message) 

    # Close connection to server 
    server.quit()

    return {"key": key}