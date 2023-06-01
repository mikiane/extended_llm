import lib__script_template_json
import random



"""
DATA DE TEST :

Task: task1
Prompt: identifier les tendances les plus impactantes pour l'avenir du secteur de la mobilité
Context: scenarioslogement
Input Data: 

Task: task2
Prompt: construire des scenarios sur la base des tendances suivantes
Context: 
Input Data: task1
    
"""

model = "gpt-3.5-turbo"

script="Task: task1\n\
    Prompt: identifier les tendances les plus impactantes pour l'avenir du secteur de la mobilité\n\
    Brain_id: scenarioslogement\n\
    Input Data:\n\
    Task: task2\n\
    Prompt: construire des scenarios sur la base des tendances suivantes\n\
    Brain_id:\n\
    Input Data: task1"

json_file = "tmp/test" + random.randint(0, 1000).__str__() + ".json"
output_json_file = "tmp/test_output" + random.randint(0, 1000).__str__() + ".json"

# write text to json file
lib__script_template_json.text_to_json(script, json_file)

lib__script_template_json.execute_json(json_file, output_json_file, model="gpt-4")

