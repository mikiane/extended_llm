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
import random
import streamlit as st

load_dotenv(".env") # Load the environment variables from the .env file.
DESTINATAIRES_TECH = os.environ.get("DESTINATAIRES_TECH")
PODCASTS_PATH = os.environ.get("PODCASTS_PATH")
n_feeds = 5 # define the number of feeds to get from Feedly
n_links = 3 # define the number of links to get from each feed

##########################################################################################################################################################################
# Function to get rss feed links from Feedly API by topic
def get_feedly_feeds(topic):
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
    return(rss_urls)
    
    
##########################################################################################################################################################################
# Function that parse rss feeds and return a list of links
def parse_feeds(rss_urls):
    
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
    return(rss_urls)
    
##########################################################################################################################################################################
# Function that summarize rss feeds and return a list of summaries
def summarize_feeds(rss_urls, topic):
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

    return(summaries)

##########################################################################################################################################################################
# Function that build a chronicle from a list of summaries
def build_chronicle(summaries, topic):
    # concatener les résumés 
    source = ""
    for summary in summaries:
        source += str(summary[2]) + "\n\n"
    
    # generer la chronique    
    prompt = f"Objectif : obtenir une chronique à diffuser (par email et en audio) signée par l’équipe de Brightness. \nRôle : Agis comme un rédacteur de chronique, journaliste spécialisé dans les sujets de {topic} qui rédige une chronique à destination du grand public en essayant de vulgariser au mieux, sans dénaturer la complexité du sujet traité.\nTache : Ecrire une chronique à partir des éléments de contexte.\nEtapes : Commencer directement par un des éléments du contexte et développer la chronique en créant des liaisons entre les différents articles traités.\nFormat : Adopter un ton dynamique, style radio. Sauter des lignes entre chaque article traité. Ecrire tous les chiffres, les têtes de chapitre éventuels, les nombres, les dates en toutes lettres. Le texte ne doit pas comporter de parenthèses ni de tirets."
    site = ""
    input_data = source
    chronicle = execute(prompt, site, input_data, model)
     
    return(chronicle)

##########################################################################################################################################################################
# Function that generate a prompte to build an image
def generate_podcast(text, topic):
    # generer titre
    titre = f"Revue de presse {topic} \n du \n" + str(date.today())

    #id_podcast
    randint = random.randint(0, 100000)
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
    
    return(id_podcast)

    # titre = "Dailywatch \n du \n" + str(date.today())
    # input_audiofile = filename
    # output_videofile = "datas/podcast" + str(randint) + ".mp4"

    ## creation de la video avec les fichiers d'entrée appropriés
    # create_video_with_audio(input_audiofile, titre, output_videofile)


##########################################################################################################################################################################
# Function that generate sources from a list of links
def generate_sources(rss_urls):
    # generer les sources
    sources = "sources: \n"
    for site_name, url, link_title in rss_urls:  # add site_name
        sources += link_title + ": " + url + "\n\n"
    
    return(sources)

##########################################################################################################################################################################
# Function that generate an illustration from a text
def generate_illustration(text, id_podcast):
    # generer image ###############@
    # generation du prompt pour la génération de l'image
    prompt_image = request_llm("Décrire une illustration pour cette chronique en présisant les détails visuels en moins de 240 caractères", '', text, "gpt-3.5-turbo")
    output_filename = "img/" + id_podcast + ".png"
    generate_image(prompt_image, output_filename)
    ############################################

##########################################################################################################################################################################
# Function that send an email with the chronicle and the illustration
def send_email(chronicle, final_filename, topic, sources, output_filename, destinataires):
    # Votre code pour envoyer le courriel ici
    today = date.today()
    formatted_date = today.strftime('%d/%m/%Y')
    titre =  str(formatted_date) + f' Revue de presse {topic}'
    text = chronicle + "\n\n" + "Aller plus loin :" + "\n\n" + sources
    audio = final_filename
    image = output_filename

    st.write("envoi de l'email")
    ## envoyer par email
    for destinataire in destinataires:
        mailfile(titre, audio, image, destinataire, text)



def main():
    st.title("Générateur de podcasts Brightness AI")
    destinataires_input = st.text_input('Saisissez les adresses e-mail des destinataires de la chronique et du podcast, séparées par une virgule : ')
    if destinataires_input:
        destinataires = [email.strip() for email in destinataires_input.split(",")]
    else:
        destinataires = []
        
        
    topic = st.text_input('Veuillez saisir un sujet de veille : ')
    
    if topic:
        feeds = get_feedly_feeds(topic)

        st.header("Sources & URLs")
        for feed in feeds:
            st.write(' / '.join(feed))
        
        confirmation = st.button("Voulez-vous continuer avec ces sources ?")

        if confirmation:
            parsed_feeds = parse_feeds(feeds)

            st.header("Sélectionnez vos articles")
            selected_indices = st.multiselect("Veuillez sélectionner les urls que vous souhaitez conserver", 
                                                options=range(1, len(parsed_feeds)+1), 
                                                format_func=lambda x: f"{x}. {parsed_feeds[x-1]}")

            parsed_feeds = [parsed_feeds[i-1] for i in selected_indices]

            st.header("Génération de la chronique...")
            summaries = summarize_feeds(parsed_feeds, topic)
            chronicle = build_chronicle(summaries, topic)
            id_podcast = generate_podcast(chronicle, topic)
            sources = generate_sources(parsed_feeds)
            generate_illustration(chronicle, id_podcast)
            final_filename = PODCASTS_PATH + "final_podcast" + id_podcast + ".mp3"
            output_filename = "img/" + id_podcast + ".png"
            send_email(chronicle, final_filename, topic, sources, output_filename, destinataires)
            
            st.success(f"Le podcast pour le sujet '{topic}' a été créé et envoyé par mail.")
        else:
            st.warning("Veuillez ajuster vos sources et recommencer.")
            feed = st.text_input("saisir un flux RSS à traiter : ")
            n_links = st.number_input("saisir le nombre de liens à traiter (max 5): ", max_value=5)
            if feed and n_links:
                feeds = [["Feed", feed]]

if __name__ == "__main__":
    main()
