
from lib_agent_buildchronical import *

# récupérer le parametre prompt passé en argument argv[1] du script
# prompt = sys.argv[1]


text = "Une planète Terre illuminée, avec des icônes symbolisant les sujets principaux de la chronique : un barrage brisé en Ukraine, une raquette de tennis pour Roland-Garros, un gavel pour la politique française, et des avions pour les patrouilles sino-russes."
filename = "img/test.png"
generate_image(text, filename)

output_filename = 'img/output_image.png'

