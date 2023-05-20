
import lib__embedded_context

    
####################### MAIN ##############################
## testing the functions
text = "<add your query>"
# ex : text = "What is the capital of France ?" 

index_filename = '<filename of the indexfile generated with build index>'
# ex : index_filename = 'files/emb_csv_1584.csv'

print(lib__embedded_context.query_extended_llm(text, index_filename, "gpt-4"))

###########################################################