from chunking.vectordb import search_chunks

def retrieve_repo_context(question):
    results = search_chunks(question)	
    return results