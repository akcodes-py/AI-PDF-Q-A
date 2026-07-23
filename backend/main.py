import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our custom modules
from pdf_reader import get_text_from_pdf, split_text_into_chunks
from embedder import make_embeddings_for_chunks, find_best_chunks
from ask_ai import get_answer_from_ai

app = FastAPI()

# Enable CORS for frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for chunks and embeddings (resets when server restarts)
global_store = {
    "chunks": [],
    "embeddings": []
}

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "AI PDF Q&A Tool Backend is running!"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Accepts a PDF file, extracts text, chunks it, embeds it, and stores in memory.
    """
    # Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 1. Extract text from PDF
        full_text = get_text_from_pdf(temp_file_path)
        if not full_text.strip():
            return {"error": "Could not extract text from the PDF. It might be scanned or empty."}
            
        # 2. Split text into chunks
        chunks = split_text_into_chunks(full_text, chunk_size=500)
        
        # 3. Create embeddings for the chunks
        embeddings = make_embeddings_for_chunks(chunks)
        
        # 4. Store them in our in-memory global variables
        global_store["chunks"] = chunks
        global_store["embeddings"] = embeddings
        
        return {
            "message": "PDF processed successfully!", 
            "chunks_count": len(chunks)
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Takes a question, finds relevant chunks, and gets an AI answer.
    """
    if not global_store["chunks"] or not len(global_store["embeddings"]):
        return {"error": "No PDF has been uploaded yet. Please upload a PDF first."}
        
    question = request.question
    
    # 1. Find the best matching chunks
    best_chunks = find_best_chunks(
        question, 
        global_store["chunks"], 
        global_store["embeddings"], 
        how_many=3
    )
    
    # 2. Get answer from OpenAI
    answer = get_answer_from_ai(question, best_chunks)
    
    # Return both the answer and the sources used
    return {
        "answer": answer,
        "sources": best_chunks
    }
