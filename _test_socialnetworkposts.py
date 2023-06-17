import base64
import json
from requests_oauthlib import OAuth2Session
import linkedin
import tweepy
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

load_dotenv(".env") # Load the environment variables from the .env file.
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET") 
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
LINKEDIN_TOKEN = os.environ.get("LINKEDIN_TOKEN")


##################################################################
### Function to tweet text with Tweepy
def tweet_text(text):
    # Authentifiez-vous à l'API Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Créez une instance de l'API
    api = tweepy.API(auth)

    # Publiez un tweet
    api.update_status(text)
    
##################################################################
### Function to tweet text + video with Tweepy
def tweet_text_with_video(title, text, video_path, hashtags):
    # Authentifiez-vous à l'API Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Créez une instance de l'API
    api = tweepy.API(auth)

    # Uploadez la vidéo
    video_upload_result = api.media_upload(video_path, media_category='tweet_video')

    # Créez le texte du tweet
    tweet_text = f"{title}\n\n{text}\n\n{hashtags}"

    # Publiez un tweet avec la vidéo
    api.update_status(status=tweet_text, media_ids=[video_upload_result.media_id_string])




##################################################################
### Function to tweet text + video with Twitter API V2
# Paramètres pour OAuth2
CLIENT_ID = os.environ.get("CONSUMER_KEY")
CLIENT_SECRET = os.environ.get("CONSUMER_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

# URL pour l'authentification et l'obtention du token
AUTH_URL = "https://twitter.com/i/oauth2/authorize"
TOKEN_URL = "https://api.twitter.com/2/oauth2/token"

# Scopes nécessaires pour lire et écrire des tweets
SCOPES = ["tweet.read", "users.read", "tweet.write", "offline.access"]

# Endpoint pour l'upload de média
MEDIA_UPLOAD_URL = "https://upload.twitter.com/1.1/media/upload.json"

def tweet_text_with_video_v2(title, text, video_path, hashtags):
    # Créez une session OAuth2
    twitter = OAuth2Session(CLIENT_ID, redirect_uri='oob', scope=SCOPES)

    authorization_url, state = twitter.authorization_url(AUTH_URL)
    print('Please go to the following URL and authorize the app:\n' + authorization_url)


    authorization_response = input('Enter the full callback URL')

    # Extract the authorization code from the callback URL
    from urllib.parse import parse_qs, urlparse
    url_parts = urlparse(authorization_response)
    query = parse_qs(url_parts.query)
    authorization_code = query["code"][0]

    # Fetch the token
    token = twitter.fetch_token(
        token_url=TOKEN_URL,
        client_secret=CLIENT_SECRET,
        code=authorization_code,
    )

    
    # Ouvrez la vidéo en mode binaire
    with open(video_path, "rb") as video_file:
        video_data = video_file.read()
    
    # Encodez la vidéo en base64
    video_data_encoded = base64.b64encode(video_data).decode("utf-8")
    
    # Préparez les paramètres pour l'upload de la vidéo
    upload_params = {
        "media_category": "tweet_video",
        "media_data": video_data_encoded
    }
    
    headers = {
    "Authorization": "Bearer {}".format(token["access_token"]),
    "Content-Type": "application/json"
    }
    # Uploadez la vidéo
    upload_response = twitter.post(MEDIA_UPLOAD_URL, headers=headers, params=upload_params)

        
    # Assurez-vous que l'upload a réussi
    if upload_response.status_code == 200:
        media_id = upload_response.json().get("media_id_string")
    else:
        raise Exception("Failed to upload video: " + upload_response.text)
    
    # Créez le texte du tweet
    tweet_text = f"{title}\n\n{text}\n\n{hashtags}"
    
    # Préparez les paramètres pour le tweet
    tweet_params = {
        "status": tweet_text,
        "media_ids": media_id
    }
    
    # Postez le tweet
    tweet_response = twitter.post("https://api.twitter.com/2/tweets", params=tweet_params)
    
    # Assurez-vous que le tweet a été posté avec succès
    if tweet_response.status_code != 200:
        raise Exception("Failed to post tweet: " + tweet_response.text)



########################################################################################################################
### Fuction to post a video on linkedin with linkedin API

def post_on_linkedin(title, texte, videofile):
    # Créer une instance de l'API LinkedIn
    app = linkedin.LinkedInApplication(token=LINKEDIN_TOKEN)

    # Télécharger la vidéo
    app.upload_video(videofile, title, texte)