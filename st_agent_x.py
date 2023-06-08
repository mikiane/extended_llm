#################   Agent X   #################
# Agent récupérant les sources de veille sur Feedly, les parsant, les résument et les envoyant par mail sous la forme d'une chronique.
# Auteur : Michel Levy Provencal (Brightness AI)
# Date : 2023-06-07
#  Format : "[['AI Brightness', 'https://flint.media/bots/feeds/eyJhbGciOiJIUzI1NiJ9.eyJib3RfaWQiOjEyNzYxLCJlZGl0aW9uIjoibWF0Y2hfc2FtcGxlcyJ9.9Jha1LyxzzlEzA4xRtJqp1MD323gQZXvENePFMq8ptY']]" topic
################################################
################################################


from lib_agent_buildchronical import *
import lib__search_sources
import sys
import ast
from datetime import date
import streamlit as st




load_dotenv(".env") # Load the environment variables from the .env file.
DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")
n_feeds = 10 # define the number of feeds to get from Feedly
n_links = 2 # define the number of links to get from each feed

## INITIALISATION
st.write("\033c", end="")
st.write("Bienvenue dans le generateur de podcasts Brightness AI !\n\n")
st.write("Ce script va vous permettre de générer un podcast à partir de sources de veille.\n\n")
st.write("Il va d'abord vous demander de saisir un sujet de veille, puis il va récupérer les sources de veille sur Feedly, les parsant, les résument et les envoyant par mail sous la forme d'une chronique.\n\n")
st.write("Pour commencer, veuillez saisir un sujet de veille.\n\n")
# confirmation
topic = input("Quel sujet souhaitez-vous traiter ? ")

if topic.lower() == '':
    st.write("Le script s'est arrêté.")
    exit()
else:
    st.write("Le script continue...")


""" 
#############################################################################################################
# récupération des arguments passés en ligne de commande
try:
    topic = sys.argv[1]
except IndexError:
    st.write("Erreur : Aucun argument n'a été passé en ligne de commande")
    sys.exit(1)
#############################################################################################################    
"""

try:
    array_as_string = lib__search_sources.get_feedly_feeds(topic, n_feeds)
except Exception as e:
    st.write(f"Erreur lors de l'appel de 'get_feedly_feeds' : {e}")
    sys.exit(1)

if not array_as_string:  # c'est-à-dire, si array_as_string est vide
    st.write("Erreur : 'get_feedly_feeds' a renvoyé une chaîne vide")
    sys.exit(1)

try:
    array_as_string = repr(array_as_string)  # obtient une représentation de chaîne sûre pour ast.literal_eval
    rss_urls = ast.literal_eval(array_as_string)  # convertit la chaîne en liste
except Exception as e:
    st.write(f"Erreur lors de la conversion de la chaîne en liste : {e}")
    sys.exit(1)

##########################################################################################################################################################################
# formattage des urls
formatted_list = [' / '.join(item) for item in rss_urls]
formatted_string = '\n\n'.join(formatted_list)
st.write("\n\n Sources & URLs :\n")
st.write(formatted_string)
st.write("\n\n")

##########################################################################################################################################################################
# confirmation
confirmation = input("Voulez-vous continuer avec ces sources ? (y/n) ")

if confirmation.lower() != 'y':
    feed = input("saisir un flux RSS à traiter : ")
    n_links = input("saisir le nombre de liens à traiter (max 5): ")
    rss_urls = [["Feed", feed]]
else:
    st.write("Le script continue avec les flux spécifiés...")

##########################################################################################################################################################################
# rss_urls = [
#    ["AI Brightness", "https://flint.media/bots/feeds/eyJhbGciOiJIUzI1NiJ9.eyJib3RfaWQiOjEyNzYxLCJlZGl0aW9uIjoibWF0Y2hfc2FtcGxlcyJ9.9Jha1LyxzzlEzA4xRtJqp1MD323gQZXvENePFMq8ptY"]
# ]
##########################################################################################################################################################################  

n = int(n_links)  # define number of links to get from each feed

### Récpération des premiers articles des flux.
rss_urls_transformed = []  # a new list to store the transformed values

for site_name, rss_url in rss_urls:
    first_n_links = extract_n_links(rss_url, n)  # get the first n links from the RSS feed
    if first_n_links:  # only add the line if the result is not an empty list
        for link in first_n_links:
            link_title = extract_title(link)
            rss_urls_transformed.append([site_name, link, link_title])

rss_urls = rss_urls_transformed  # replace the original list with the transformed list

##########################################################################################################################################################################
## Affichage des liens
# formattage des urls
formatted_list = [' / '.join(item) for item in rss_urls]
formatted_string = '\n\n'.join(formatted_list)
st.write("\n\n Articles & URLs : \n")
st.write(formatted_string)
st.write("\n\n")


##########################################################################################################################################################################
# Choix des URLS à conserver
rss_urls = filter_urls(rss_urls)

st.write("\n\n Calcul des résumés...  \n")

## generer les résumés
summaries = []
for site_name, url, link_title in rss_urls:
    prompt = f"Rédige un résumé vulgarisé de cet article sur {topic}, en respectant la complexité du sujet, destiné au grand public."
    site = url
    input_data = ""
    summary = execute(prompt, site, input_data, model)
    st.write(summary)
    
    if summary is not None:  # only add the line if the result is not None
        summaries.append([link_title, url, summary])  # replace site_name with link_title

##########################################################################################################################################################################
# formattage des urls
formatted_list = [' / '.join(item) for item in summaries]
formatted_string = '\n\n'.join(formatted_list)
    

# concatener les résumés 
source = ""
for summary in summaries:
    source += str(summary[2]) + "\n\n"

st.write("\n\n Résumés concaténés : \n")   
st.write(source)
st.write("\n\n") 
   
# generer la chronique    
prompt = f"Objectif : obtenir une chronique à diffuser (par email et en audio) signée par l’équipe de Brightness. \nRôle : Agis comme un rédacteur de chronique, journaliste spécialisé dans les sujets de {topic} qui rédige une chronique à destination du grand public en essayant de vulgariser au mieux, sans dénaturer la complexité du sujet traité.\nTache : Ecrire une chronique à partir des éléments de contexte.\nEtapes : Commencer directement par un des éléments du contexte et développer la chronique en créant des liaisons entre les différents articles traités.\nFormat : Adopter un ton dynamique, style radio. Sauter des lignes entre chaque article traité. Ecrire tous les chiffres, les têtes de chapitre éventuels, les nombres, les dates en toutes lettres. Le texte ne doit pas comporter de parenthèses ni de tirets."
site = ""
input_data = source
chronicle = execute(prompt, site, input_data, model)
st.write("\n\n Voici la Chronique : \n")
st.write(chronicle) 
st.write("\n\n")

  
# generer les sources
sources = "sources: \n"
# generer les sources
sources = "sources: \n"
for site_name, url, link_title in rss_urls:  # add site_name
    sources += link_title + ": " + url + "\n\n"
st.write("\n\n Voici les sources : \n")    
st.write(sources)
st.write("\n\n")

        
# generer le podcast
# Appeler l'API elevenLabs et construire un podcast
text = chronicle
# chronicle = text = "Chers lecteurs, Dans cette édition de notre chronique, nous vous présentons les dernières avancées et découvertes dans le domaine de l'intelligence artificielle (IA), en mettant l'accent sur les travaux de recherche et les applications innovantes. \n\nVoici un résumé des articles que nous avons sélectionnés pour vous, tirés de diverses sources en ligne. \nSur le site de VentureBeat, une nouvelle méthode appelée Patch-to-Cluster attention (PaCa) a été développée pour améliorer l'efficacité des systèmes d'IA basés sur les transformateurs de vision (ViT). \n\nCette méthode permet de réduire les exigences en matière de calcul et de mémoire, tout en améliorant la capacité des ViT à identifier, classer et segmenter les objets dans les images. \n\nLes chercheurs prévoient de former PaCa sur des ensembles de données plus importants. \nDans un article publié sur le site de l'Université Drexel, des chercheurs ont développé une méthode utilisant l'IA pour évaluer les dommages dans les structures en béton armé en se basant sur les motifs de fissuration. \n\nCette approche, basée sur la théorie des graphes, permet d'obtenir une évaluation rapide et précise des dommages avec une précision supérieure à quatre-vingt-dix pour cent. \n\nLe chien de garde du terrorisme met en garde contre les menaces pour la sécurité nationale posées par l'IA, comme le rapporte le site de Jonathan Hall KC. \n\nLes créateurs d'IA sont encouragés à abandonner leur mentalité techno-utopiste et à prendre en compte les intentions des terroristes lors de la conception de la technologie Sur le site du MIT, Cindy Alejandra Heredia, étudiante en MBA, a rejoint l'équipe MIT Driverless pour travailler sur les véhicules autonomes et aider à résoudre les problèmes de mobilité dans les communautés défavorisées. \n\nL'équipe a atteint un nouveau record de vitesse de cent cinquante-deux mph lors des essais en janvier et a terminé quatrième lors de sa première participation à l'Indy Autonomous Challenge. \n\nDans un article de Medium, la leçon cinq d'un cours en sept leçons sur la conception, la mise en œuvre et le déploiement de systèmes d'apprentissage automatique (ML) en utilisant les bonnes pratiques MLOps est présentée. \n\nLa leçon se concentre sur la validation des données et la surveillance en temps réel des performances du modèle. \n\nEnfin, sur le blog de Google AI, les chercheurs présentent AVFormer, une méthode simple pour intégrer des informations visuelles dans les modèles de reconnaissance automatique de la parole (ASR) existants. \n\nCette approche vise à améliorer la robustesse des systèmes ASR en utilisant des indices visuels provenant de vidéos multimodales. \n\nNous espérons que ces informations vous seront utiles et vous aideront à rester informés des dernières avancées dans le domaine de l'IA. \n\nN'hésitez pas à partager cette chronique avec vos collègues et amis intéressés par l'IA. \n\nCordialement. L'équipe de Brightness. \n\n"

# generer titre
titre = f"Revue de presse {topic} \n du \n" + str(date.today())

#id_podcast
randint = randint(0, 100000)
id_podcast = str(randint) + str(date.today())

# generer image ###############@
# generation du prompt pour la génération de l'image
prompt_image = request_llm("Décrire une illustration pour cette chronique en présisant les détails visuels en moins de 240 caractères", '', text, "gpt-3.5-turbo")
output_filename = "img/" + id_podcast + ".png"
generate_image(prompt_image, output_filename)
############################################

# creation de l'audio
#voice_id = "DnF3PZl1PUQOKY4LvcUl" # MLP
voice_id = "TxGEqnHWrfWFTfGW9XjX"  # Josh
final_filename = PODCASTS_PATH + "final_podcast" + id_podcast + ".mp3"

# gestion des intonations.
split_text(text, limit=300)
convert_and_merge(text, voice_id, final_filename)

# titre = "Dailywatch \n du \n" + str(date.today())
# input_audiofile = filename
# output_videofile = "datas/podcast" + str(randint) + ".mp4"

## creation de la video avec les fichiers d'entrée appropriés
# create_video_with_audio(input_audiofile, titre, output_videofile)

today = date.today()
formatted_date = today.strftime('%d/%m/%Y')
titre =  str(formatted_date) + f' Revue de presse {topic}'
text = chronicle + "\n\n" + "Aller plus loin :" + "\n\n" + sources
audio = final_filename
destinataires = ["michel@brightness.fr","mlevypro@gmail.com"]
image = output_filename

st.write("envoi de l'email")
## envoyer par email
mailfile(titre, audio, image, destinataires, text)

st.write("All done!")


