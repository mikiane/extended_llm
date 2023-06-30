# ----------------------------------------------------------------------------
# Project: Semantic Search Module for the Alter Brain project
# File:    lib__search_source.py
#  Uses Feedly to fiond RSS feeds based on a topic
# 
# Author:  Michel Levy Provencal
# Brightness.ai - 2023 - contact@brightness.fr
# ----------------------------------------------------------------------------

import requests
from dotenv import load_dotenv
import os
from lib__path import *

#Récupération des sites de veille via Feedly
load_dotenv(DOTENVPATH)

#load_dotenv(".env") # Load the environment variables from the .env file.
FEEDLY_API_TOKEN = os.environ.get("FEEDLY_API_TOKEN")
api_token = FEEDLY_API_TOKEN

# Function to get the feedly feeds (n = number of feeds, topic = topic to search)
def get_feedly_feeds(topic, n=3):
    url = 'https://cloud.feedly.com/v3/search/feeds'
    headers = {'Authorization': 'OAuth ' + api_token}
    params = {'query': topic, 'count': n}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f'Error with status code: {response.status_code}')
        return []
    
    data = response.json()
    feeds = []
    
    for result in data.get('results', []):
        title = result.get('title')
        feed_url = result.get('feedId', '').replace('feed/', '')
        feeds.append([title, feed_url])
    #print (str(feeds))
    return feeds
    
    
