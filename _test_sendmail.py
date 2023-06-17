
from dotenv import load_dotenv
import os
from moviepy.editor import *
from datetime import date
from lib_agent_buildchronical import mailfile

load_dotenv(".env") # Load the environment variables from the .env file.

DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")


titre = 'Daily Watch Tech du ' + str(date.today())
text = "ceci est un test"
audio = "datas/podcasts/podcast71373.mp3"
destinataires = ["michel@brightness.fr", "mlevypro@gmail.com"]

## envoyer par email
mailfile(titre, audio, destinataires, text)