

# ----------------------------------------------------------------------------
# Project: Flask API for the Alter Brain project
# File:    alter_brain_api.py
#
# This file is a part of the project "Alter Brain"
# It's a Flask API to build the index from a folder of files contained in the file sent in the POST request
# and to query the index with a text Request
#
# Author:  Michel Levy Provencal
# Brightness.ai - 2023 - contact@brightness.fr
# ----------------------------------------------------------------------------

"""
Run your application: You can run your Flask application locally using the command line. To do so, navigate to the directory containing your .py file (e.g., app.py) and run the following command:
python alter_brain_api.py
This command will start a Flask development server on your machine. By default, it will be accessible at http://127.0.0.1:5000/ or http://localhost:5000/.
Send a POST request: You can test the /buildindex route by sending a POST request. You can use tools like Postman or curl for this. The request should include a file in the request body. Here's how you can do it with curl:
curl -X POST -F "file=@path_to_your_file" http://localhost:5000/buildindex
Replace "path_to_your_file" with the file path you want to send.
Check the response: After sending the request, you should receive a response from your Flask server. You can inspect this response to ensure it contains the expected information.
Check server content: Additionally, you can check the content of your server to ensure that the file has been received and processed correctly. For example, you can check if the folder has been created as expected and if the file has been properly extracted or saved.
"""


import lib__embedded_context
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import time
from zipfile import ZipFile
import shutil
import sendmail

# Base folder path
base_folder = "datas/"

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask application
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Limit the size of uploaded files to 100 MB


# API buildindex : to build the index from a folder of files contained in the file sent in the POST request
@app.route('/buildindex', methods=['POST'])
def handle_file():
    """
    This function processes the file submitted in the POST request.
    It creates a directory with the name of the file (without the extension) and a timestamp.
    If the file is a zip file, it extracts all the files inside it to the base of the created directory.
    If it's not a zip file, it saves the file to the created directory.
    Finally, it calls the index_folder function with the created directory name.
    """

    # Vérifier si un fichier a été fourni
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    uploaded_file = request.files['file']
    
    email = request.form.get('email')

    # Vérifier si le nom du fichier est vide
    if uploaded_file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    # Récupérer le nom de base du fichier et créer un nouveau nom de dossier avec un timestamp
    base_name = os.path.splitext(uploaded_file.filename)[0]
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    folder_name = f"{base_folder}{base_name}_{timestamp}/"

    # Créer le nouveau dossier
    os.makedirs(folder_name, exist_ok=True)

    # Si le fichier est un zip, le dézipper
    if uploaded_file.filename.endswith('.zip'):
        with ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall(folder_name)
    else:
        # Si le fichier n'est pas un zip, le sauvegarder dans le nouveau dossier
        file_path = os.path.join(folder_name, uploaded_file.filename)
        uploaded_file.save(file_path)
    
    # Appeler la fonction d'indexation sur le nouveau dossier
    lib__embedded_context.build_index(folder_name)

    brain_id = base_name + "_" + timestamp
    # Créer la réponse JSON
    res = [{'id':1, 'request':'buildindex', 'answer':brain_id}]
    response = jsonify(res)
    response.headers['Content-Type'] = 'application/json'
    
    #Send the Brain_id to the email
    sendmail.mailfile(email, None, ' Votre index est prêt. Son brain_id est : ' + brain_id)

    
    # NOTE : the index is in the folder : base_folder + base_name + "_" + timestamp + "/" + emb_index.csv

    return response

# API searchcontext : to search the context of a request in the index (brain id and request are passed in the POST request) 
@app.route('/searchcontext', methods=['POST'])
def handle_req():
    """
    This function searches for the context of a request in the index.
    It retrieves the text and index parameters from the POST request form.
    The index filename is constructed based on the provided index parameter.
    It calls the `find_context` function from the `lib__embedded_context` module
    with the text, index filename, and number of results.
    The function returns a JSON response containing the search results.

    :return: A JSON response with the search results.
    """
    
    text = request.form.get('request')
    index = request.form.get('brain_id')
    index_filename = "datas/" + index + "/emb_index.csv"
    
    # si le brain_id a la forme d'une url (http ou https), on crée un index specifique à l'url
    
    if index.startswith("http://") or index.startswith("https://"):
        url = index
        index_filename= "datas/" + lib__embedded_context.build_index_url(url) + "/emb_index.csv"
        #index_filename = index_filename
    
    context = lib__embedded_context.find_context(text, index_filename, n_results=3)
    res = [{'id':1,'request':'searchcontext','answer':context}]
    response = jsonify(res)
    response.headers['Content-Type'] = 'application/json'
    return(response)
    
    
    


if __name__ == '__main__':
    app.run(debug=True)
