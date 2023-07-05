import PyPDF2
import os

# Spécifiez le répertoire contenant les fichiers PDF
pdf_directory = '/Users/michel/Desktop/BNP'

# Parcourir tous les fichiers dans le répertoire
for filename in os.listdir(pdf_directory):
    # Vérifiez si le fichier est un PDF
    if filename.endswith('.pdf'):
        # Créer le chemin complet vers le fichier PDF
        pdf_path = os.path.join(pdf_directory, filename)
        
        # Ouvrez le fichier PDF
        with open(pdf_path, 'rb') as file:
            # Créez un objet lecteur PDF
            reader = PyPDF2.PdfReader(file)
            
            # Créez un fichier texte avec le même nom que le fichier PDF
            txt_path = os.path.join(pdf_directory, filename.replace('.pdf', '.txt'))
            
            # Ouvrez le fichier texte en mode écriture
            with open(txt_path, 'w') as txt_file:
                # Parcourir toutes les pages du PDF
                for page_num in range(len(reader.pages)):
                    # Extraire le texte de la page
                    text = reader.pages[page_num].extract_text()
                    # Écrire le texte dans le fichier TXT
                    txt_file.write(text)

print("Conversion terminée")
