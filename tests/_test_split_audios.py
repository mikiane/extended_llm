from datetime import date
from pydub import AudioSegment
from random import randint
from elevenlabs import set_api_key
from dotenv import load_dotenv
import os
from moviepy.editor import *
import requests

load_dotenv(".env")  # Load the environment variables from the .env file.
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")

def split_text(text, limit=1000):
    """
    This function splits the text into chunks of around 1000 characters. \n
    It splits before a newline character.
    """
    chunks = []
    current_chunk = ""
    
    for line in text.split('\n'):
        if len(current_chunk) + len(line) <= limit:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk = line + "\n"

    # Append the last chunk
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def texttospeech(text, voice_id, filename):
    """
    This function calls the Eleven Labs API to convert text to speech
    """
    try:
        set_api_key(ELEVENLABS_API_KEY)
        CHUNK_SIZE = 1024
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
        }

        data = {
        "text": text,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.95,
            "similarity_boost": 1
            }
        }

        response = requests.post(url, json=data, headers=headers)

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
    
    except requests.RequestException as e:
        print(f"Failed to convert text to speech: {e}")
        return
    
def convert_and_merge(text, voice_id, final_filename):
    """
    This function splits the text, converts each chunk to speech and merges all the resulting audio files.
    """
    chunks = split_text(text)
    filenames = []

    # Add intro sequence to the beginning
    combined = AudioSegment.from_mp3("sounds/intro.mp3")

    for i, chunk in enumerate(chunks):
        filename = f"{i}.mp3"
        filenames.append(filename)
        texttospeech(chunk, voice_id, filename)
        
        # Concatenate each audio segment
        audio_segment = AudioSegment.from_mp3(filename)
        combined += audio_segment

    # Add outro sequence to the end
    combined += AudioSegment.from_mp3("sounds/outro.mp3")

    # Save the final concatenated audio file
    combined.export(final_filename, format='mp3')

    # Delete temporary audio files
    for filename in filenames:
        os.remove(filename)






voice_id = "TxGEqnHWrfWFTfGW9XjX"  # Josh
randint = randint(0, 100000)
final_filename = PODCASTS_PATH + "final_podcast" + str(randint) + str(date.today()) + ".mp3"
text = "Chers lecteurs, Dans cette édition de notre chronique, nous vous présentons les dernières avancées et découvertes dans le domaine de l'intelligence artificielle (IA), en mettant l'accent sur les travaux de recherche et les applications innovantes. \n\nVoici un résumé des articles que nous avons sélectionnés pour vous, tirés de diverses sources en ligne. \nSur le site de VentureBeat, une nouvelle méthode appelée Patch-to-Cluster attention (PaCa) a été développée pour améliorer l'efficacité des systèmes d'IA basés sur les transformateurs de vision (ViT). \n\nCette méthode permet de réduire les exigences en matière de calcul et de mémoire, tout en améliorant la capacité des ViT à identifier, classer et segmenter les objets dans les images. \n\nLes chercheurs prévoient de former PaCa sur des ensembles de données plus importants. \nDans un article publié sur le site de l'Université Drexel, des chercheurs ont développé une méthode utilisant l'IA pour évaluer les dommages dans les structures en béton armé en se basant sur les motifs de fissuration. \n\nCette approche, basée sur la théorie des graphes, permet d'obtenir une évaluation rapide et précise des dommages avec une précision supérieure à quatre-vingt-dix pour cent. \n\nLe chien de garde du terrorisme met en garde contre les menaces pour la sécurité nationale posées par l'IA, comme le rapporte le site de Jonathan Hall KC. \n\nLes créateurs d'IA sont encouragés à abandonner leur mentalité techno-utopiste et à prendre en compte les intentions des terroristes lors de la conception de la technologie Sur le site du MIT, Cindy Alejandra Heredia, étudiante en MBA, a rejoint l'équipe MIT Driverless pour travailler sur les véhicules autonomes et aider à résoudre les problèmes de mobilité dans les communautés défavorisées. \n\nL'équipe a atteint un nouveau record de vitesse de cent cinquante-deux mph lors des essais en janvier et a terminé quatrième lors de sa première participation à l'Indy Autonomous Challenge. \n\nDans un article de Medium, la leçon cinq d'un cours en sept leçons sur la conception, la mise en œuvre et le déploiement de systèmes d'apprentissage automatique (ML) en utilisant les bonnes pratiques MLOps est présentée. \n\nLa leçon se concentre sur la validation des données et la surveillance en temps réel des performances du modèle. \n\nEnfin, sur le blog de Google AI, les chercheurs présentent AVFormer, une méthode simple pour intégrer des informations visuelles dans les modèles de reconnaissance automatique de la parole (ASR) existants. \n\nCette approche vise à améliorer la robustesse des systèmes ASR en utilisant des indices visuels provenant de vidéos multimodales. \n\nNous espérons que ces informations vous seront utiles et vous aideront à rester informés des dernières avancées dans le domaine de l'IA. \n\nN'hésitez pas à partager cette chronique avec vos collègues et amis intéressés par l'IA. \n\nCordialement. L'équipe de Brightness. \n\n"
split_text(text, limit=450)
convert_and_merge(text, voice_id, final_filename)