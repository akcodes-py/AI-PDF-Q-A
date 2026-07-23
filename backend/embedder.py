import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model once when this file is imported
model = SentenceTransformer('all-MiniLM-L6-v2')

def make_embedding(text):
    """
    Returns the embedding vector for a single piece of text.
    """
    return model.encode(text)

def make_embeddings_for_chunks(chunks):
    """
    Returns embeddings for a list of text chunks.
    """
    return model.encode(chunks)

def cosine_similarity(vector_a, vector_b):
    """
    Calculates the cosine similarity between two vectors using numpy.
    """
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return dot_product / (norm_a * norm_b)

def find_best_chunks(question, chunks, chunk_embeddings, how_many=3):
    """
    Finds the top 'how_many' matching chunks for a given question.
    """
    question_embedding = make_embedding(question)
    
    scored_chunks = []
    for i, chunk_embedding in enumerate(chunk_embeddings):
        score = cosine_similarity(question_embedding, chunk_embedding)
        scored_chunks.append((score, chunks[i]))
        
    # Sort by score in descending order (highest score first)
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    # Return just the text of the top chunks
    best_chunks = [chunk for score, chunk in scored_chunks[:how_many]]
    return best_chunks
