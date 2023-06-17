import os
import argparse
from lib_agent_buildchronical import *
from dotenv import load_dotenv

def create_podcast(voice_id, text_file, id_podcast):
    load_dotenv(".env") # Load the environment variables from the .env file.
    PODCASTS_PATH = os.environ.get("PODCASTS_PATH")

    # Read the text from the file
    with open(text_file, 'r') as file:
        text = file.read()

    # creation de l'audio
    final_filename = os.path.join(PODCASTS_PATH, "final_podcast" + id_podcast + ".mp3")

    # gestion des intonations.
    convert_and_merge(text, voice_id, final_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a podcast from text.')
    parser.add_argument('voice_id', type=str, help='The ID of the voice to use.')
    parser.add_argument('text_file', type=str, help='The text file to convert to a podcast.')
    parser.add_argument('id_podcast', type=str, help='The ID of the podcast.')
    args = parser.parse_args()
    create_podcast(args.voice_id, args.text_file, args.id_podcast)
