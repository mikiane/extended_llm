extended_llm

# WORK IN PROGRESS #

A simplified version of a second brain for neural language models using simple CSV files containing embeddings.

This Python code implements a system for understanding and processing natural language to facilitate information retrieval based on semantics rather than traditional keyword-based search. It uses the OpenAI Embedding API to generate text embeddings from blocks of text. These embeddings are stored in CSV files that constitute a semantic index. A text query is compared to the index's embeddings to find the most similar text blocks. These similar text blocks provide a context that is used to query a neural language model such as GPT-4. The language model's response can then be used to complete or generate new knowledge from the original query.


- create a folder with all the txt files you want to index & request
- create a .env file with your [OPENAI_API_KEY=sk-XXXXX] in it
- START by building an index file using build_index.py
- REQUEST the index file using query_extedend_llm.py
- Adapt the code of query_extedend_llm.py to test

Works with GPT4
Soon with LLAMA...


