from lib_agent_buildchronical import *
from datetime import date
from pydub import AudioSegment
from random import randint
from elevenlabs import set_api_key
from dotenv import load_dotenv
import os
from moviepy.editor import *

load_dotenv(".env")  # Load the environment variables from the .env file.
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")

voice_id = "TxGEqnHWrfWFTfGW9XjX"  # Josh
randint = randint(0, 100000)
filename = PODCASTS_PATH + "podcast" + str(randint) + str(date.today()) + ".mp3"
text = "Chers lecteurs, Dans cette édition de notre chronique, nous vous présentons les dernières avancées et découvertes dans le domaine de l'intelligence artificielle (IA), en mettant l'accent sur les travaux de recherche et les applications innovantes. \nVoici un résumé des articles que nous avons sélectionnés pour vous, tirés de diverses sources en ligne. \nSur le site de VentureBeat, une nouvelle méthode appelée Patch to Cluster attention (PaCa) a été développée pour améliorer l'efficacité des systèmes d'IA basés sur les transformateurs de vision (ViT). \nCette méthode permet de réduire les exigences en matière de calcul et de mémoire, tout en améliorant la capacité des ViT à identifier, classer et segmenter les objets dans les images. \nLes chercheurs prévoient de former PaCa sur des ensembles de données plus importants. \nDans un article publié sur le site de l'Université Drexel, des chercheurs ont développé une méthode utilisant l'IA pour évaluer les dommages dans les structures en béton armé en se basant sur les motifs de fissuration. \nCette approche, basée sur la théorie des graphes, permet d'obtenir une évaluation rapide et précise des dommages avec une précision supérieure à quatre-vingt-dix pour cent. Le chien de garde du terrorisme met en garde contre les menaces pour la sécurité nationale posées par l'IA, comme le rapporte le site de Jonathan Hall KC. \nLes créateurs d'IA sont encouragés à abandonner leur mentalité techno-utopiste et à prendre en compte les intentions des terroristes lors de la conception de la technologie Sur le site du MIT, Cindy Alejandra Heredia, étudiante en MBA, a rejoint l'équipe MIT Driverless pour travailler sur les véhicules autonomes et aider à résoudre les problèmes de mobilité dans les communautés défavorisées. \nL'équipe a atteint un nouveau record de vitesse de cent cinquante-deux mph lors des essais en janvier et a terminé quatrième lors de sa première participation à l'Indy Autonomous Challenge. Dans un article de Medium, la leçon cinq d'un cours en sept leçons sur la conception, la mise en œuvre et le déploiement de systèmes d'apprentissage automatique (ML) en utilisant les bonnes pratiques MLOps est présentée. La leçon se concentre sur la validation des données et la surveillance en temps réel des performances du modèle. Enfin, sur le blog de Google AI, les chercheurs présentent AVFormer, une méthode simple pour intégrer des informations visuelles dans les modèles de reconnaissance automatique de la parole (ASR) existants. Cette approche vise à améliorer la robustesse des systèmes ASR en utilisant des indices visuels provenant de vidéos multimodales. \nNous espérons que ces informations vous seront utiles et vous aideront à rester informés des dernières avancées dans le domaine de l'IA. N'hésitez pas à partager cette chronique avec vos collègues et amis intéressés par l'IA. \nCordialement, L'équipe de Brightness"
texttospeech(text, voice_id, filename)
