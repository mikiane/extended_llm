from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
import mimetypes
import os



load_dotenv(".env") # Load the environment variables from the .env file.
SENDGRID_KEY = os.getenv('SENDGRID_KEY') # assuming the key is stored as 'SENDGRID_KEY' in your .env file

def mailfile(destinataire='michel@brightness.fr', filename=None, message=""):
    message = Mail(
        from_email='contact@brightness.fr',
        to_emails=destinataire,
        subject='Le résultat du traitement',
        plain_text_content='Votre demande a été traité.' + message
    )
    
    if filename:
        with open(filename, 'rb') as f:
            data = f.read()

        encoded = base64.b64encode(data).decode()
        mime_type = mimetypes.guess_type(filename)[0]

        attachedFile = Attachment(
           FileContent(encoded),
           FileName(filename),
           FileType(mime_type),
           Disposition('attachment')
        )
        message.attachment = attachedFile

    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    
    
