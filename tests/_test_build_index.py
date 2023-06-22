
import lib__embedded_context
import sendmail
import os
import time
from zipfile import ZipFile
# Test the build_index(folder_path) function
# Path to index : files/

# get the zip file from http post request



# generate a folder name with a timestamp


# unzip the file in the folder


#folder_path = '<path to the folder containing the files to index>'
# careful : only txt files.
base_folder = "datas/"
email = "michel@brightness.fr"
uploaded_file = "startupsmedia123.zip"

# Récupérer le nom de base du fichier et créer un nouveau nom de dossier avec un timestamp
base_name = os.path.splitext(uploaded_file)[0]
timestamp = time.strftime("%Y%m%d-%H%M%S")
folder_name = f"{base_folder}{base_name}_{timestamp}/"

# Créer le nouveau dossier
print("creation du folder_name s'il n'existe pas : " + folder_name)
os.makedirs(folder_name, exist_ok=True)

def is_a_zip(uploaded_file):
    _, extension = os.path.splitext(uploaded_file)
    return extension == '.zip'

# Si le fichier est un zip, le dézipper
if is_a_zip(uploaded_file):
    with ZipFile(base_folder + uploaded_file, 'r') as zip_ref:
        print("extraction zip")
        zip_ref.extractall(folder_name)

    
print("folder_name for build_index : " + folder_name)
# Appeler la fonction d'indexation sur le nouveau dossier
lib__embedded_context.build_index(folder_name)

brain_id = base_name + "_" + timestamp

print("brain_id : " + brain_id)
#Send the Brain_id to the email
sendmail.mailfile(email, None, ' Votre index est prêt. Son brain_id est : ' + brain_id)


