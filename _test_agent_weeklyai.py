from lib_agent_buildchronical import *

load_dotenv(".env") # Load the environment variables from the .env file.
DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")

"""
TRAITEMENT DES TACHES
"""

# Task: task1
prompt = "Exraire l'article le plus récent publié sur la homepage de AI News et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "https://www.artificialintelligence-news.com/"
input_data = ""
task1 = execute(prompt, brain_id, input_data, model)
print(task1)
# Task: task2

prompt = "Exraire l'article le plus récent publié  sur la homepage de MIT Technology Review - AI et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "https://www.technologyreview.com/artificial-intelligence/"
input_data = ""
task2 = execute(prompt, brain_id, input_data, model)
print(task2)
# Task: task3

prompt = "Exraire l'article le plus récent publié sur la homepage de Artificial Intelligence on Medium et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "https://medium.com/topic/artificial-intelligence"
input_data = ""
task3 = execute(prompt, brain_id, input_data, model)
print(task3)
# Task: task4

prompt = "Exraire l'article le plus récent publié sur la homepage de Toward Data Science et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "https://towardsdatascience.com/"
input_data = ""
task4 = execute(prompt, brain_id, input_data, model)
print(task4)    
# Task: task5

prompt = "Exraire l'article le plus récent publié sur la homepage de Google AI Blog et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "https://ai.googleblog.com/"
input_data = ""
task5 = execute(prompt, brain_id, input_data, model)
print(task5)
# Task: task6

prompt = "Exraire l'article le plus récent publié sur la homepage de ArXiv Sanity Preserver et les reformuler (en affichant la source de chaque article) sous la forme d'une revue de presse."
brain_id = "http://www.arxiv-sanity.com/"
input_data = ""
task6 = execute(prompt, brain_id, input_data, model)
print(task6)
# Task: task7

prompt = "Reformuler l'ensemnle des articles qui suivent en citant le site où ils ont été extraits (écrire les chiffres et nombres en toutes lettres). A partir de ces éléments rédiger une chronique à diffuser par email signée par 'l'équipe de Brightness A I. "
brain_id = ""
input_data = task6 + "\n" + task5 + "\n" + task4 + "\n" + task3 + "\n" +  task2 + "\n" +  task1
task7 = execute(prompt, brain_id, input_data, model)

print(task7)
# Task : task7

# Appeler l'API elevenLabs et construire un podcast
text = task7

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


titre = 'Daily Watch AI du ' + str(date.today())
text = text
audio = filename
destinataires = ["michel@brightness.fr","mlevypro@gmail.com"]

## envoyer par email
mailfile(titre, audio, destinataires, text)