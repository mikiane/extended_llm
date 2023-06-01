
import lib__embedded_context

    
####################### MAIN ##############################
## testing the functions
#text = "<add your query>"
text = "\
    Role : Tu es un consultant spécialiste de la stratégie.\
    Tache : Tu dois repenser le positionnement et la manière de présenter l’agence Brightness.\
    Objectif : Optimiser la manière de présenter l’agence Brightness à ses prospects ainsi que ses offres, compte tenu du marché actuel.\
    Contrainte : Il faut garder en tête que l’événemntiel rapporte beaucoup mais est très concurrentiel et que les offres de conseil et de formation sont des offres couteuses mais d’avenir. la formation coute mais c’est une offre d’avenir.\
    Etapes : Trouver les 3 principaux concurrents de facon global puis les 3 concurrents sur chacune des offres de Brightness. Sur la base de ces éléments, trouver des éléments différentiateurs. Rédiger une nouvelle manière de présenter Brightness et ses offres (par exemple sous la forme d’un mail type ou d’une présentation sur la home page du site de Brightness). \
    Format : Un texte d’une longueur de plus de 5000 signes.\
    "
model = "gpt-4"
#index_filename = '<filename of the indexfile generated with build index>'
index_filename = 'datas/brightness.output/brightness.outputemb_csv_7794.csv'

print(lib__embedded_context.query_extended_llm(text, index_filename, model))


###########################################################