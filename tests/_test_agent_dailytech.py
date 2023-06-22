from lib_agent_buildchronical import *

load_dotenv(".env") # Load the environment variables from the .env file.
DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")

"""
TRAITEMENT DES TACHES
"""

# Task: task1
# Prompt = "Exraire les informations publiées sur la homepage de MIT Technology Review et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
# Brain_id: https://www.technologyreview.com/
# Input Data:
prompt = "Exraire les informations publiées sur la homepage de MIT Technology Review et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "https://www.technologyreview.com/"
input_data = ""
task1 = execute(prompt, brain_id, input_data, model)


# Task: task2
# Prompt: Extraire les informations publiées sur la homepage de Futurism et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse.
# Brain_id: https://futurism.com/
# Input Data: task1
Prompt = "Extraire les informations publiées sur la homepage de Futurism et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "https://futurism.com/"
input_data = task1
task2 = execute(prompt, brain_id, input_data, model)


# Task: task3
# Prompt: Extraire les informations publiées sur la homepage de Wired et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse.
# Brain_id: https://www.wired.com/
# Input Data: task2
prompt = "Extraire les informations publiées sur la homepage de Wired et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "https://www.wired.com/"
input_data = task2
task3 = execute(prompt, brain_id, input_data, model)

# Task: task4
# Prompt: Extraire les informations publiées sur la homepage de Futurity et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse.
# Brain_id: https://www.futurity.org/
# Input Data: task3
prompt = "Extraire les informations publiées sur la homepage de Futurity et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "https://www.futurity.org/"
input_data = task3
task4 = execute(prompt, brain_id, input_data, model)


# Task: task5
# Prompt: Extraire les informations publiées sur la homepage de Next Big Future et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse.
# Brain_id: https://www.nextbigfuture.com/
# Input Data: task4
prompt = "Extraire les informations publiées sur la homepage de Next Big Future et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "https://www.nextbigfuture.com/"
input_data = task4
task5 = execute(prompt, brain_id, input_data, model)


# Task: task6
# Prompt: Reformuler la revue de presse Dailywatch de sorte à en faire une chronique intégrant les news (en affichant la source de chaque article) de MIT Technology Review,  Futurism, Futurity, Next Big Future et Wired diffusée par email.
# Brain_id:
# Input Data: task5+task4+task3+task2+task1
prompt = "Reformuler l'ensemnle des articles en citant la source de chaque article. Ecrire les chiffres et nombres, dates ou années en toutes lettres, et en faire une chronique à diffuser par email signée par 'l'équipe de Brightness A I. "
brain_id = ""
input_data = task5 + "\n" + task4 + "\n" + task3 + "\n" +  task2 + "\n" +  task1
task6 = execute(prompt, brain_id, input_data, model)


# Task : task7

# Appeler l'API elevenLabs et construire un podcast
text = task6

# creation de l'audio
#voice_id = "DnF3PZl1PUQOKY4LvcUl" # MLP
voice_id = "TxGEqnHWrfWFTfGW9XjX" # Josh
randint = randint(0, 100000)
filename = PODCASTS_PATH + "podcast" + str(randint) + ".mp3"
texttospeech(text, voice_id, filename)

# titre = "Dailywatch \n du \n" + str(date.today())
# input_audiofile = filename
# output_videofile = "datas/podcast" + str(randint) + ".mp4"

## creation de la video avec les fichiers d'entrée appropriés
# create_video_with_audio(input_audiofile, titre, output_videofile)


titre = 'Daily Watch Tech du ' + str(date.today())
text = text
audio = filename
destinataires = ["michel@brightness.fr","mlevypro@gmail.com"]

## envoyer par email
mailfile(titre, audio, destinataires, text)