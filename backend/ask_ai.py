import os
import google.generativeai as genai

def get_answer_from_ai(question, best_chunks):
    """
    Calls the Gemini API to answer the question using only the provided chunks.
    """
    # Read API key from environment
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable is not set."
        
    genai.configure(api_key=api_key)
    
    # Combine the best chunks into one context string
    context = "\n\n---\n\n".join(best_chunks)
    
    # Build a prompt that strictly restricts the AI to the given context
    system_instruction = (
        "You are a helpful assistant that answers questions based ONLY on the provided document context. "
        "If the answer is not contained in the text, you must say exactly: "
        "'I could not find that in the document'. "
        "Do not make up information. Keep your answer brief, about 3-4 sentences maximum."
    )
    
    user_message = f"Context from document:\n{context}\n\nQuestion: {question}"
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
        response = model.generate_content(user_message)
        # Return the text of the answer
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {e}"
