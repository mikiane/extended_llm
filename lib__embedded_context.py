

# ----------------------------------------------------------------------------
# Project: Semantic Search Module
# File:    lib__embedded_context.py
# 
# This lib is part of the Semantic Search Module project. It implements a 
# system for understanding and processing natural language to facilitate 
# information retrieval based on semantics rather than traditional keyword-based search.
# 
# Author:  Michel Levy Provencal
# Brightness.ai - 2023 - contact@brightness.fr
# ----------------------------------------------------------------------------

import pandas as pd
import os
import csv
import openai
from openai.embeddings_utils import get_embedding
from transformers import GPT2TokenizerFast
from dotenv import load_dotenv
import random
import numpy as np
import sys
import time
import requests



"""
#############################################################################################################
    
    ## TOOLS
    
#############################################################################################################
"""




# ----------------------------------------------------------------------------
# Function that concat all files contained in a folder in a text
def concat_files_in_text(path):
    """
    Concatenates the files of a directory into a single text.
    :param path: Directory path.
    :return: Concatenated text.
    """    
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    texts = []
    for file in files:
        with open(file, 'r') as f:
            texts.append(f.read())
    return ' '.join(texts)
# ----------------------------------------------------------------------------




# ----------------------------------------------------------------------------
# Function that split the txt file into blocks. Uses batch (limit) of 2000 words with gpt3.5 and 4000 with gpt4
def split_text_into_blocks(text, limit=4000):
    
    """
    This function splits a given text into chunks, or "blocks", each containing a certain number of words specified by the 'limit' parameter. It's particularly designed for use with GPT-3.5 (limit of 2000 words) and GPT-4 (limit of 4000 words).
    Each block is constructed by sequentially adding words from the input text until the block size (the number of words in the block) reaches the limit. If adding another word would exceed the limit, the function checks for the last sentence or line delimiter in the current block (a period or newline character), then separates the block at that delimiter.
    If there is no delimiter in the current block, the entire block is added to the list of blocks and the next word starts a new block. If a delimiter is found, the block is split at the delimiter, and the remaining text (if any) is added to the next block along with the next word.
    The function returns a list of blocks.
    :param text: The input text to be split into blocks.
    :param limit: The maximum number of words allowed in each block. Default is 4000.
    :return: A list of text blocks obtained from the input text.
    """
    ### TODO : Adapt the limit to other LLMs (LLAMAS, All-GPT, etc.)
    
    blocks = []
    current_block = ""
    words = text.split()

    for word in words:
        if len(current_block + word) + 1 < limit:
            current_block += word + " "
        else:
            last_delimiter_index = max(current_block.rfind(". "), current_block.rfind("\n"))

            if last_delimiter_index == -1:
                blocks.append(current_block.strip())
                current_block = word + " "
            else:
                delimiter = current_block[last_delimiter_index]
                blocks.append(current_block[:last_delimiter_index + (1 if delimiter == '.' else 0)].strip())
                current_block = current_block[last_delimiter_index + (2 if delimiter == '.' else 1):].strip() + " " + word + " "

    if current_block.strip():
        blocks.append(current_block.strip())

    return blocks

# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
# Function that write blocks into filename
def write_blocks_to_csv(blocks, path, filename):
    """
    This function takes a list of blocks (data items) and a filename as input parameters, then writes these blocks into a CSV file specified by the given filename.
    The blocks are written row by row in the CSV file, with each block making up a single row. 
    The CSV file is created with a specific encoding (UTF-8), and using specific settings for delimiter and quotechar for CSV data formatting.
    :param blocks: A list of data items to be written into the CSV file.
    :param filename: The name of the CSV file where the data should be written.
    """
    with open(path + filename, "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Write the header
        csvwriter.writerow(['Datas'])

        for block in blocks:
            csvwriter.writerow([block])
# ----------------------------------------------------------------------------




# ----------------------------------------------------------------------------
# Function that gets the embedding for a given text
def get_embedding(text, engine="text-embedding-ada-002"):
    """
    This function takes in a piece of text and a model engine as input parameters, and returns an embedding for the input text. 
    It utilizes OpenAI's Embedding API to generate the embedding based on the specified model.

    The function first replaces newline characters in the input text with spaces, as the embedding models typically 
    handle single continuous strings of text.

    :param text: The input text for which to generate an embedding.
    :param engine: The model engine to use for generating the embedding. Default is 'text-embedding-ada-002'.
    :return: The generated embedding for the input text.
    """
    
    text = text.replace("\n", " ")
    ############################################################################################################      
    #### DEBUG
    print("get embedding for " + text)
    ############################################################################################################
    return openai.Embedding.create(input = [text], model=engine)['data'][0]['embedding']
   


# ----------------------------------------------------------------------------
# Function that creates embeddings for text data in a specified CSV file
def create_embeddings(path, filename):
    """
    This function reads text data from a specified CSV file and creates embeddings for each text entry using OpenAI's
    Embedding API. It then saves the generated embeddings back to a new CSV file.

    The function uses a GPT-2 tokenizer to tokenize the text data. It then filters out rows where the number of tokens
    exceeds 8000 and keeps the last 2000 records. The function also drops rows with missing values from the data.

    The embeddings are generated using the 'text-embedding-ada-002' model by default, and the generated embeddings are 
    saved as a new column in the DataFrame.

    The function finally saves the DataFrame, with the embeddings, to a new CSV file.

    :param path: The directory path where the input and output CSV files are located.
    :param filename: The name of the input CSV file from which to read the text data.
    """
    load_dotenv(".env") # Load the environment variables from the .env file.
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
       
    # Open the input CSV file and read it into a Pandas DataFrame.
    # Read the CSV file using the ';' separator and ignoring incorrect lines.
    df_full = pd.read_csv(path + filename, sep=';', error_bad_lines=False, encoding='utf-8')
    
    ############################################################################################################      
    #### DEBUG
    print("file loaded")
    ############################################################################################################


    #rename the dataframe's columns
    df = df_full[['Datas']]
    print("df loaded with " + str(len(df)) + " rows")

    #remove rows with missing values 
    df = df.dropna()
    ############################################################################################################      
    #### DEBUG
    print("df cleaned with " + str(len(df)) + " rows")
    ############################################################################################################

    # A new column 'n_tokens' is added to the DataFrame 'df'. The values in this column are computed by applying a 
    # lambda function to each value in the 'Datas' column of the DataFrame. 
    # This lambda function uses a tokenizer to encode the text data and then counts the number of tokens in the encoded result.
    
    # And filter the DataFrame, keeping only the rows where 'n_tokens' is less than 8000.
    # It then selects the last 2000 records from this filtered DataFrame. 
    df['n_tokens'] = df.Datas.apply(lambda x: len(tokenizer.encode(x)))
    df = df[df.n_tokens<8000].tail(2000)
    
    ############################################################################################################      
    #### DEBUG
    print("df cleaned with " + str(len(df)) + " rows") 
    ############################################################################################################      
    
         
    df['ada_embedding'] = df.Datas.apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))
    ############################################################################################################      
    #### DEBUG
    print("embeddings created")
    ############################################################################################################      

    # write the value of the vector from the dataframe in a second CSV file named emb_xxx.csv
    df.to_csv(path + "emb_" + filename, index=False)





# ----------------------------------------------------------------------------
# Function that reads and processes a CSV file and returns a DataFrame
def read_and_process_csv(index_filename):
    """
    This function takes as input the filename of a CSV file and reads this file into a Pandas DataFrame. 
    It then processes the 'ada_embedding' column of the DataFrame, converting the string representations 
    of embeddings stored in this column back into actual Numpy array objects.

    The function first reads the CSV file using Pandas' read_csv function, creating a DataFrame where each 
    row corresponds to a data item from the CSV file and each column corresponds to a field in the data items.

    It then applies the eval function to each item in the 'ada_embedding' column to convert the string 
    representations of the embeddings back into list objects. These lists are then further converted into 
    Numpy arrays using the np.array function. This processed 'ada_embedding' column replaces the original 
    column in the DataFrame.

    :param index_filename: The filename of the CSV file to read.
    :return: The DataFrame created from the CSV file, with the 'ada_embedding' column processed.
    """
    
    df = pd.read_csv(index_filename)
    df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)
    return df



# ----------------------------------------------------------------------------
# Function that gets an embedding vector for a given text
def get_search_vector(text):
    """
    This function takes as input a piece of text and returns an embedding vector for the input text. 
    It utilizes the 'get_embedding' function to generate the 
    embedding vector.

    The function is a convenience wrapper around the 'get_embedding' function, simplifying its use by 
    directly passing the input text and relying on the 'get_embedding' function's default parameters 
    for generating the embedding.

    :param text: The input text for which to generate an embedding vector.
    :return: The embedding vector for the input text.
    """

    return get_embedding(text)



# ----------------------------------------------------------------------------
# Function that finds similar rows in a DataFrame based on an input vector
def find_similar_rows(df, searchvector, n_results):
    """
    This function takes as input a DataFrame, a search vector, and a number of results to return.
    It calculates the cosine similarity between the search vector and the embeddings in the DataFrame. 
    The rows with the highest cosine similarity are then sorted and the top 'n_results' rows are returned.

    The function adds a new column, 'similarities', to the DataFrame. For each row, it computes the dot 
    product between the 'ada_embedding' of the row and the search vector, which is equivalent to calculating 
    the cosine similarity when the vectors are normalized.

    The rows in the DataFrame are then sorted in descending order of 'similarities', and the top 'n_results' 
    rows are returned as a new DataFrame.

    :param df: The input DataFrame, each row of which should have an 'ada_embedding' column containing a vector.
    :param searchvector: The vector to compare against the 'ada_embedding' of each row in the DataFrame.
    :param n_results: The number of top similar rows to return.
    :return: A DataFrame containing the top 'n_results' similar rows to the input vector.
    """

    df['similarities'] = df.ada_embedding.apply(lambda x: np.dot(x, searchvector))
    res = df.sort_values('similarities', ascending=False).head(n_results)
    return res


# ----------------------------------------------------------------------------
# Function that validates a DataFrame and extracts the combined data
def validate_and_get_combined(res):
    """
    This function takes a DataFrame as input, performs several validation checks on it, 
    and then extracts and returns the combined data from the 'Datas' column of the DataFrame.

    The function first checks if the 'Datas' column exists in the DataFrame. If it does not, 
    a ValueError is raised. It then checks if the DataFrame is empty. If it is, a ValueError 
    is raised. Finally, it checks if the index of the DataFrame is of type 'int64'. If it is 
    not, a ValueError is raised.

    Once these validation checks have passed, the function concatenates all the strings in the 
    'Datas' column of the DataFrame, with each string separated by a newline character. This combined 
    string is then returned.

    :param res: The input DataFrame to validate and extract combined data from.
    :return: A string consisting of all the data from the 'Datas' column of the DataFrame, concatenated with newline characters.
    """
    
    if 'Datas' not in res.columns:
        raise ValueError("La colonne 'Datas' n'existe pas dans le DataFrame")

    if res.empty:
        raise ValueError("Le DataFrame est vide")

    if res.index.dtype != 'int64':
        raise ValueError("L'index du DataFrame n'est pas de type entier")

    return '\n'.join(res['Datas'].values)



"""
#############################################################################################################
    
    ## FUNCTIONS TO INDEX & SEARCH EMBEDDINGS
    
#############################################################################################################
"""

## ----------------------------------------------------------------------------
## Function that creates a csv index file containing embeddings, from a folder named path. 
## The index is stored in the same folder, and named : emb_csv_XXX.csv
## The function returns the name of the index file : emb_csv_XXX.csv
## (while the concatenated text is stored in a txt file named txt_XXX.txt and the csv file containing the blocks is named csv_XXX.csv)
def build_index(folder_path):
    """
    This function reads multiple text files from a specified folder, concatenates the text, 
    splits the concatenated text into blocks of specified length, writes these blocks into a CSV file, 
    creates embeddings for each block using the create_embeddings function, and finally, saves the 
    embeddings back to the CSV file.

    The function first generates a random number which is used to create unique filenames for the 
    intermediate text and CSV files. It then reads and concatenates all the text files from the 
    specified folder into a single string of text.

    The function then calls the split_text_into_blocks function to split the text into blocks of 
    up to 4000 characters each. The resulting list of blocks is written to a new CSV file.

    The function then calls the create_embeddings function to create embeddings for each text block 
    in the CSV file. The embeddings are saved back to the CSV file.

    Finally, the function returns the name of the CSV file containing the embeddings.

    :param folder_path: The directory path where the text files are located and where the CSV file will be saved.
    :return: The name of the CSV file containing the embeddings.
    """
    
    # Concatenate files in text
    text = concat_files_in_text(folder_path)

    # Save text in a txt file named txt_(random number).txt
    random_num = random.randint(1000,9999)  # Generates a random number between 1000 and 9999

    # Call the function split_text_into_blocks() to split the text into blocks
    blocks = split_text_into_blocks(text, limit=4000)

    # Call the function write_blocks_to_csv() to write the blocks into a csv file
    write_blocks_to_csv(blocks, folder_path, f'csv_{random_num}.csv')

    # Create embeddings for the csv file
    create_embeddings(folder_path, f'csv_{random_num}.csv')
    
    return(f'emb_csv_{random_num}.csv')


# ----------------------------------------------------------------------------
# Function that finds the context for a given query in an index file
def find_context(text, index_filename, n_results=3):
    """
    This function takes as input a piece of text, the filename of a CSV file containing indexed data, 
    and an optional number of results to return. It finds the most similar data items to the input 
    text in the indexed data and returns the combined data from these items.

    The function first loads environment variables from a .env file, including the OpenAI API key. 
    It then reads and processes the indexed data from the CSV file into a DataFrame.

    The function creates an embedding for the input text using the get_search_vector function. 
    This embedding is compared with the embeddings of the data items in the DataFrame to find 
    the most similar items.

    The most similar items are sorted by their similarity scores, and the top 'n_results' items are 
    selected. The combined data from these items is extracted and returned.

    :param text: The input text for which to find similar data items.
    :param index_filename: The filename of the CSV file containing the indexed data.
    :param n_results: The number of most similar data items to return. Default is 3.
    :return: The combined data from the most similar data items.
    """
    load_dotenv(".env")  # Load the environment variables from the .env file.
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    df = read_and_process_csv(index_filename)

    searchvector = get_search_vector(text)

    res = find_similar_rows(df, searchvector, n_results)

    return validate_and_get_combined(res)




# ----------------------------------------------------------------------------
# Function that queries the OpenAI language model with a context and query
def query_extended_llm(text, index_filename, model="gpt-4"):
    """
    This function takes as input a piece of text, the filename of a CSV file containing indexed data, 
    and an optional AI model to use. It queries the OpenAI language model with a context derived from 
    the most similar data items to the input text, and a prompt derived from the input text itself. 
    It returns the response from the language model.

    The function first finds the context for the input text using the find_context function. It then 
    loads environment variables from a .env file, including the OpenAI API key. 

    The function then enters a loop where it attempts to query the language model with the context and 
    the input text as a prompt. If it encounters an exception during this process, it waits for 5 seconds 
    and then tries again, up to a maximum of 10 attempts.

    If the function is able to successfully query the language model, it returns the model's response as 
    a string. If it is unable to do so after 10 attempts, it prints an error message and terminates the 
    program.

    :param text: The input text for which to query the language model.
    :param index_filename: The filename of the CSV file containing the indexed data.
    :param model: The AI model to use for the query. Default is 'gpt-4'.
    :return: The response from the language model.
    """
    context = find_context(text, index_filename)
    load_dotenv(".env") # Load the environment variables from the .env file.

    attempts = 0
    prompt = "Context : " + context + "\n\n" + "Query : " + text
    
    api_key = os.environ.get("OPENAI_API_KEY")
    system = "Je suis un assistant parlant parfaitement le français et l'anglais capable de corriger, rédiger, paraphraser, traduire, résumer, développer des textes."

    while attempts < 10:
        try:
            url = 'https://api.openai.com/v1/chat/completions'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            data = {
                'model': 'gpt-4',
                #'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'user', 'content': prompt},
                    {'role': 'system', 'content': system}
                ]
            }
            response = requests.post(url, headers=headers, json=data)
            json_data = response.json()
            message = json_data['choices'][0]['message']['content']
            return message.strip()
        
        except Exception as e:
            error_code = type(e).__name__
            error_reason = str(e)
            attempts += 1
            print(f"Erreur : {error_code} - {error_reason}. Nouvel essai dans 5 secondes...")
            time.sleep(5)

    print("Erreur : Echec de la création de la completion après 5 essais")
    sys.exit()
