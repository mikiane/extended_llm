
# ----------------------------------------------------------------------------
# Project: Semantic Search Module for the Alter Brain project
# File:    lib__agent_buildchronical.py
#  Set of functions to build a chronic based on feeds
# 
# Author:  Michel Levy Provencal
# Brightness.ai - 2023 - contact@brightness.fr
# ----------------------------------------------------------------------------



from random import randint
from elevenlabs import set_api_key
from dotenv import load_dotenv
from lib__script_template_json import truncate_strings, request_llm
import os
from urllib.parse import unquote
from queue import Queue
from pydub import AudioSegment
from moviepy.editor import *
from datetime import date
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
import mimetypes
import requests
from bs4 import BeautifulSoup
from datetime import date
from pydub import AudioSegment
from random import randint
from elevenlabs import set_api_key
from dotenv import load_dotenv
import os
from moviepy.editor import *
import requests
import json
from PIL import Image, ImageDraw, ImageFont
from num2words import num2words
import re


model="gpt-4"
#model = "gpt-3.5-turbo"

load_dotenv("/home/michel/extended_llm/.env")  # Load the environment variables from the .env file.
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")
SENDGRID_KEY = os.environ.get("SENDGRID_KEY")



def replace_numbers_with_text(input_string):
    
    # Remplacer les pourcentages
    percentages = re.findall(r'\d+%', input_string)
    for percentage in percentages:
        number = percentage[:-1]
        number_in_words = num2words(number, lang='fr')
        input_string = input_string.replace(percentage, f"{number_in_words} pour cent")
    
    # Remplacer les nombres
    numbers = re.findall(r'\b\d+\b', input_string)
    for number in numbers:
        number_in_words = num2words(number, lang='fr')
        input_string = input_string.replace(number, number_in_words)
    
    return input_string




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





##################################################################
### Function to convert text to speech with Eleven Labs API
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
    combined = AudioSegment.from_mp3("/home/michel/extended_llm/sounds/intro.mp3")

    for i, chunk in enumerate(chunks):
        filename = f"{i}.mp3"
        filenames.append(filename)
        texttospeech(chunk, voice_id, filename)
        
        # Concatenate each audio segment
        audio_segment = AudioSegment.from_mp3(filename)
        combined += audio_segment

    # Add outro sequence to the end
    combined += AudioSegment.from_mp3("/home/michel/extended_llm/sounds/outro.mp3")

    # Save the final concatenated audio file
    combined.export(final_filename, format='mp3')

    # Delete temporary audio files
    for filename in filenames:
        os.remove(filename)




def mailfile(title, audio, text, email):
    """
    Fonction pour envoyer un e-mail avec une pièce jointe via SendGrid.
    
    Args:
        audio (str): Le chemin vers le fichier à joindre.
        image (str) : Le chemin vers le fichier image à joindre.
        destinataire (str): L'adresse e-mail du destinataire.
        message (str, optional): Un message à inclure dans l'e-mail. Par défaut, le message est vide.
    """
    # Création de l'objet Mail
    message = Mail(
        from_email='contact@brightness.fr',
        to_emails=email,
        subject=title,
        plain_text_content=text)
    
    # Ajout des destinataires en BCC
    # for email in destinataires:
    message.add_bcc('contact@mikiane.com')
        
    # Lecture du fichier audio à joindre
    with open(audio, 'rb') as f:
        data_audio = f.read()

    # Encodage du fichier audio en base64
    encoded_audio = base64.b64encode(data_audio).decode()
    
    # Détermination du type MIME du fichier audio
    mime_type_audio = mimetypes.guess_type(audio)[0]
    
    # Création de l'objet Attachment pour l'audio
    attachedFile_audio = Attachment(
        FileContent(encoded_audio),
        FileName(audio),
        FileType(mime_type_audio),
        Disposition('attachment')
    )
    message.add_attachment(attachedFile_audio)

    # Lecture du fichier image à joindre
    #with open(image, 'rb') as f:
    #    data_image = f.read()

    # Encodage du fichier image en base64
    #encoded_image = base64.b64encode(data_image).decode()
    
    # Détermination du type MIME du fichier image
    #mime_type_image = mimetypes.guess_type(image)[0]
    
    # Création de l'objet Attachment pour l'image
    #attachedFile_image = Attachment(
    ##    FileContent(encoded_image),
    #    FileName(image),
    #    FileType(mime_type_image),
    #    Disposition('attachment')
    #)
    #message.add_attachment(attachedFile_image)

    # Tentative d'envoi de l'e-mail via SendGrid
    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
        print("\n")
        print(str(e))



########################################################################################################################
## Function that return the first feed from an RSS feed
import feedparser
def extract_first_link(rss_url):
    feed = feedparser.parse(rss_url)
    if len(feed.entries) > 0:
        return feed.entries[0].link
    else:
        return None


########################################################################################################################
## Function that return the first n feed from an RSS feed

def extract_n_links(rss_url, n):
    feed = feedparser.parse(rss_url)
    links = []
    for i in range(min(n, len(feed.entries))):
        links.append(feed.entries[i].link)
    return links


########################################################################################################################
## Function that rextract a title from a web page basedon its url

def extract_title(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        return soup.title.string
    except AttributeError:
        return "No Title Found"


########################################################################################################################
### Function execute a prompt with the OpenAI API / with some context (brain_id, ur or input_data) and return the result



def execute(prompt, site, input_data, model="gpt-4"):
    # extract news from url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    
    context = ""
    if site:  # only proceed if site is not empty
        try:
            response = requests.get(site, headers=headers)
            response.raise_for_status()  # raise exception if invalid response
            
            soup = BeautifulSoup(response.content, "html.parser")
            # remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            context = soup.get_text()
        except (requests.RequestException, ValueError):
            print(f"Failed to get content from {site}.")

    prompt, context, input_data = truncate_strings(prompt, context, input_data, 6000)
    
    if model == "gpt-4":
        # Limitation des erreurs de longueur
        prompt, context, input_data = truncate_strings(prompt, context, input_data, 12000)
        
    if model == "gpt-3.5-turbo-16k":
        # Limitation des erreurs de longueur
        prompt, context, input_data = truncate_strings(prompt, context, input_data, 24000)
    
    print("TRAITEMENT DU PROMPT : \n")
    print("prompt : ", prompt, "\n")
    print("context : ", context, "\n")
    print("input_data : ", input_data, "\n")
    print("model : ", model, "\n")
        
    # Appel au LLM
    res = request_llm(prompt, context, input_data, model)
    return (res)




########################################################################################################################
### Function that create a video with a text and an audio file



def create_video_with_audio(input_audio, input_text, output_file):
    # Convertir le fichier MP3 en WAV
    audio = AudioSegment.from_mp3(input_audio)
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")

    # Créer le clip audio à partir du fichier WAV
    audio_clip = AudioFileClip(wav_path)

    # Créer le clip vidéo avec un fond noir et le texte au centre
    text_size = 40  # Taille de police initiale
    txt_clip = TextClip(input_text, fontsize=text_size, color='white', size=(500, 500))
    while txt_clip.w > 500 or txt_clip.h > 500:
        # Réduire la taille de police jusqu'à ce que le texte tienne dans le cadre
        text_size -= 5
        txt_clip = TextClip(input_text, fontsize=text_size, color='white', size=(500, 500))
    txt_clip = txt_clip.set_position('center').set_duration(audio_clip.duration)

    # Fusionner le clip audio et le clip vidéo
    video_clip = CompositeVideoClip([txt_clip.set_audio(audio_clip)])

    # Écrire la vidéo résultante au format mp4 avec le format de pixel spécifié
    video_clip.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=24, 
                               ffmpeg_params=['-pix_fmt', 'yuv420p'])

    # Supprimer le fichier temporaire WAV
    os.remove(wav_path)




########################################################################################################################
# Function that create an image with a text and an image file
def create_image_with_text(text, input_file, output_file):
    # Ouvrir l'image existante
    img = Image.open(input_file)

    # Marge désirée
    margin = 30

    # Créez un objet de dessin
    draw = ImageDraw.Draw(img)

    # Déterminer la taille de la police à utiliser
    fontsize = 1  # commencer par une petite taille de police
    font = ImageFont.truetype("font/arial.ttf", fontsize)

    # Augmenter la taille de la police jusqu'à ce que le texte soit trop large
    while draw.textsize(text, font=font)[0] < img.width - 2*margin:
        fontsize += 1
        font = ImageFont.truetype("font/arial.ttf", fontsize)

    # Réduire la taille de la police d'un pas pour ne pas dépasser la largeur de l'image
    fontsize -= 1
    font = ImageFont.truetype("font/arial.ttf", fontsize)

    # Obtenir la largeur et la hauteur du texte
    textwidth, textheight = draw.textsize(text, font)

    # Calculer les coordonnées du centre
    x = (img.width - textwidth) // 2
    y = (img.height - textheight) // 2

    # Ajouter le texte avec un contour
    outline_amount = 3
    shadowcolor = "black"
    fillcolor = "white"

    for adj in range(outline_amount):
        # Déplacer un pixel...
        draw.text((x-adj, y), text, font=font, fill=shadowcolor)
        draw.text((x+adj, y), text, font=font, fill=shadowcolor)
        draw.text((x, y-adj), text, font=font, fill=shadowcolor)
        draw.text((x, y+adj), text, font=font, fill=shadowcolor)

    # Maintenant, dessinez le texte en blanc, mais en utilisant notre copie originale de l'image
    draw.text((x, y), text, font=font, fill=fillcolor)

    # Sauvegardez l'image
    img.save(output_file)






########################################################################################################################
### Function that generate an image with a text
def generate_image(text, output_filename):
    
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
    "prompt": text,
    "n": 1,
    "size": "1024x1024"
    }

    response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, data=json.dumps(data))

    # Récupérer l'URL de la première image
    image_url = response.json()['data'][0]['url']

    # Télécharger l'image
    image_response = requests.get(image_url)

    # Écrire l'image dans un fichier
    with open(output_filename, 'wb') as f:
        f.write(image_response.content)


########################################################################################################################
# Function that allows to select the RSS feeds to keep
def filter_urls(rss_urls):
    # Affichez chaque url avec son index
    for i, url in enumerate(rss_urls):
        print(f"{i+1}. {url}")

    # Demandez à l'utilisateur de sélectionner les indices des urls à conserver
    selected_indices = input("Veuillez entrer les numéros des urls que vous souhaitez conserver, séparés par des virgules : ")

    # Convertissez les indices sélectionnés en une liste d'entiers
    selected_indices = list(map(int, selected_indices.split(',')))

    # Filtrer rss_urls pour ne conserver que les urls sélectionnées
    rss_urls = [rss_urls[i-1] for i in selected_indices]
    
    return rss_urls