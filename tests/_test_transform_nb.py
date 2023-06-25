import sys
sys.path.append("..")  # Chemin vers le répertoire parent
from lib_agent_buildchronical import replace_numbers_with_text
# Exemple d'utilisation
input_string = """Cher Michel, Bienvenue dans la chronique Brightness, votre rendez-vous incontournable pour tout savoir sur l'innovation dans les médias ! Aujourd'hui, nous vous proposons un tour d'horizon des dernières avancées en matière d'intelligence artificielle dans le journalisme, ainsi que les tendances de la consommation d'information dans le monde.
Commençons par l'intelligence artificielle (IA) et son impact sur le journalisme. Certains s'inquiètent de voir les journalistes remplacés par des machines, mais nous préférons y voir une opportunité pour améliorer et diversifier le travail des rédactions. Par exemple, la chaîne de télévision finlandaise Yle a utilisé l'IA pour traduire ses articles en ukrainien, touchant ainsi un public plus large. 
Cette technologie a permis à quelques personnes de produire un grand nombre d'articles dans une langue qu'elles ne maîtrisaient pas forcément.
Mais l'IA ne se limite pas à la traduction. Elle peut également aider les journalistes à mieux comprendre les attentes de leurs lecteurs en analysant leurs comportements et en proposant des articles susceptibles de les intéresser. L'Associated Press utilise l'IA pour rédiger des articles financiers depuis 2016, laissant ainsi plus de temps aux journalistes pour se consacrer à des enquêtes approfondies.
Maintenant, penchons-nous sur les tendances de la consommation d'information dans le monde. Selon une étude réalisée par le Reuters Institute for the Study of Journalism, Facebook perd de son influence en tant que source d'actualités, avec seulement 28% des personnes interrogées déclarant y accéder en 2023, contre 42% en 2016.
En revanche, YouTube et TikTok connaissent une forte croissance en tant que sources d'informations. TikTok est utilisé par 44% des 18-24 ans à des fins diverses, et par 20% d'entre eux pour les actualités. Les utilisateurs de TikTok, Instagram et Snapchat préfèrent les influenceurs aux journalistes, ce qui représente un défi pour les médias traditionnels sur ces plateformes.
De plus, les réseaux sociaux gagnent en importance en tant que source d'actualités, au détriment des applications et des sites web des médias. Les plateformes sociales sont omniprésentes et attirent de plus en plus l'attention des consommateurs d'informations.
Enfin, en ce qui concerne la France, 36% des Français évitent parfois ou souvent activement l'actualité. De plus, seulement 11% des Français paient pour des actualités en ligne.
Voilà pour les grandes tendances de la consommation d'information dans le monde. Nous vous donnons rendez-vous prochainement pour découvrir les dernières innovations dans le domaine des médias et de l'information. Restez connecté !
L'équipe de Brightness
Aller plus loin :"""

output_string = replace_numbers_with_text(input_string)
print(output_string)

