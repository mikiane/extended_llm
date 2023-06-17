from lib_agent_buildchronical import *

load_dotenv(".env") # Load the environment variables from the .env file.
DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")

"""
TRAITEMENT DES TACHES
"""

rss_urls = [
    ["Engaging Experiences Brightness", "https://flint.media/bots/feeds/eyJhbGciOiJIUzI1NiJ9.eyJib3RfaWQiOjExMjYwLCJlZGl0aW9uIjoibGFzdCJ9.ZmOdjbAToYBZPZnAehSeLF9oSP-9aqTuklm-6rGWYw0"]
]

n = 5  # define n

### Récpération des premiers articles des flux.
rss_urls_transformed = []  # a new list to store the transformed values

for site_name, rss_url in rss_urls:
    first_n_links = extract_n_links(rss_url, n)  # get the first n links from the RSS feed
    if first_n_links:  # only add the line if the result is not an empty list
        for link in first_n_links:
            link_title = extract_title(link)
            rss_urls_transformed.append([site_name, link, link_title])

rss_urls = rss_urls_transformed  # replace the original list with the transformed list



## generer les résumés
summaries = []
for site_name, url, link_title in rss_urls:
    prompt = "Exraire les points clés de cet article sur le thème de l'événementiel RH et les reformuler sous la forme d'un résumé en français vulgarisé pour du grand public sans dénaturer la complexité du sujet traité."
    site = url
    input_data = ""
    summary = execute(prompt, site, input_data, model)
    print(summary)
    
    if summary is not None:  # only add the line if the result is not None
        summaries.append([link_title, url, summary])  # replace site_name with link_title

# concatener les résumés 
source = ""
for summary in summaries:
    source += str(summary[2]) + "\n\n"
   
   
# generer la chronique    
prompt = "Objectif : obtenir une chronique à diffuser (par email et en audio) signée par l’équipe de Brightness. \nRôle : Agis comme un rédacteur de chronique, journaliste spécialisé dans les sujets RH qui rédige une chronique à destination du grand public en essayant de vulgariser au mieux, sans dénaturer la complexité du sujet traité.\nTache : Ecrire une chronique à partir des éléments de contexte.\nEtapes : Commencer directement par un des éléments du contexte et développer la chronique en créant des liaisons entre les différents articles traités.\nFormat : Adopter un ton dynamique, style radio. Sauter des lignes entre chaque article traité. Ecrire tous les chiffres, les têtes de chapitre éventuels, les nombres, les dates en toutes lettres. Le texte ne doit pas comporter de parenthèses ni de tirets."
site = ""
input_data = source
chronicle = execute(prompt, site, input_data, model)
print(chronicle)    
  
# generer les sources
sources = "sources: \n"
# generer les sources
sources = "sources: \n"
for site_name, url, link_title in rss_urls:  # add site_name
    sources += link_title + ": " + url + "\n"
print(sources)


        
# generer le podcast
# Appeler l'API elevenLabs et construire un podcast
text = chronicle
# chronicle = text = "Chers lecteurs, Dans cette édition de notre chronique, nous vous présentons les dernières avancées et découvertes dans le domaine de l'intelligence artificielle (IA), en mettant l'accent sur les travaux de recherche et les applications innovantes. \n\nVoici un résumé des articles que nous avons sélectionnés pour vous, tirés de diverses sources en ligne. \nSur le site de VentureBeat, une nouvelle méthode appelée Patch-to-Cluster attention (PaCa) a été développée pour améliorer l'efficacité des systèmes d'IA basés sur les transformateurs de vision (ViT). \n\nCette méthode permet de réduire les exigences en matière de calcul et de mémoire, tout en améliorant la capacité des ViT à identifier, classer et segmenter les objets dans les images. \n\nLes chercheurs prévoient de former PaCa sur des ensembles de données plus importants. \nDans un article publié sur le site de l'Université Drexel, des chercheurs ont développé une méthode utilisant l'IA pour évaluer les dommages dans les structures en béton armé en se basant sur les motifs de fissuration. \n\nCette approche, basée sur la théorie des graphes, permet d'obtenir une évaluation rapide et précise des dommages avec une précision supérieure à quatre-vingt-dix pour cent. \n\nLe chien de garde du terrorisme met en garde contre les menaces pour la sécurité nationale posées par l'IA, comme le rapporte le site de Jonathan Hall KC. \n\nLes créateurs d'IA sont encouragés à abandonner leur mentalité techno-utopiste et à prendre en compte les intentions des terroristes lors de la conception de la technologie Sur le site du MIT, Cindy Alejandra Heredia, étudiante en MBA, a rejoint l'équipe MIT Driverless pour travailler sur les véhicules autonomes et aider à résoudre les problèmes de mobilité dans les communautés défavorisées. \n\nL'équipe a atteint un nouveau record de vitesse de cent cinquante-deux mph lors des essais en janvier et a terminé quatrième lors de sa première participation à l'Indy Autonomous Challenge. \n\nDans un article de Medium, la leçon cinq d'un cours en sept leçons sur la conception, la mise en œuvre et le déploiement de systèmes d'apprentissage automatique (ML) en utilisant les bonnes pratiques MLOps est présentée. \n\nLa leçon se concentre sur la validation des données et la surveillance en temps réel des performances du modèle. \n\nEnfin, sur le blog de Google AI, les chercheurs présentent AVFormer, une méthode simple pour intégrer des informations visuelles dans les modèles de reconnaissance automatique de la parole (ASR) existants. \n\nCette approche vise à améliorer la robustesse des systèmes ASR en utilisant des indices visuels provenant de vidéos multimodales. \n\nNous espérons que ces informations vous seront utiles et vous aideront à rester informés des dernières avancées dans le domaine de l'IA. \n\nN'hésitez pas à partager cette chronique avec vos collègues et amis intéressés par l'IA. \n\nCordialement. L'équipe de Brightness. \n\n"


# creation de l'audio
#voice_id = "DnF3PZl1PUQOKY4LvcUl" # MLP
voice_id = "TxGEqnHWrfWFTfGW9XjX"  # Josh
randint = randint(0, 100000)
final_filename = PODCASTS_PATH + "final_podcast" + str(randint) + str(date.today()) + ".mp3"

# gestion des intonations.
split_text(text, limit=450)
convert_and_merge(text, voice_id, final_filename)

# titre = "Dailywatch \n du \n" + str(date.today())
# input_audiofile = filename
# output_videofile = "datas/podcast" + str(randint) + ".mp4"

## creation de la video avec les fichiers d'entrée appropriés
# create_video_with_audio(input_audiofile, titre, output_videofile)


titre = 'Daily Watch événementiel RH du ' + str(date.today())
text = chronicle + "\n\n" + "Aller plus loin :" + "\n\n" + sources
audio = final_filename
destinataires = ["michel@brightness.fr","mlevypro@gmail.com"]

## envoyer par email
mailfile(titre, audio, destinataires, text)


