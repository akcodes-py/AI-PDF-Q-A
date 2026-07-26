# AI PDF Q&A Tool

## Overview
The AI PDF Q&A Tool is a simple full-stack web application that allows users to upload a PDF document and ask questions about its content. The app generates intelligent, concise answers based strictly on the provided document.

## Architecture
1. **Upload**: User selects a PDF in the React frontend and clicks "Upload". The file is sent via FormData to the FastAPI backend.
2. **Text Extraction**: The backend uses `pdfplumber` to extract all text from the PDF.
3. **Chunking**: The extracted text is split into chunks of approximately 500 words.
4. **Embedding**: The chunks are processed by a local `sentence-transformers` model (`all-MiniLM-L6-v2`) to generate vector embeddings.
5. **Storage**: The chunks and their embeddings are temporarily stored in memory on the backend.
6. **Querying**: User types a question and clicks "Ask".
7. **Similarity Search**: The backend generates an embedding for the question and calculates cosine similarity (using `numpy`) against the stored chunk embeddings to find the top 3 most relevant chunks.
8. **AI Generation**: The top chunks and the question are sent to the Gemini API (`gemini-1.5-flash`). The AI constructs an answer strictly based on the provided context.
9. **Display**: The frontend displays the AI's answer along with the source chunks that were used to formulate it.

## Tech Stack
- **Backend**: Python, FastAPI
- **Text Extraction**: pdfplumber
- **Embeddings**: sentence-transformers (`all-MiniLM-L6-v2`)
- **Vector Operations**: numpy (Cosine Similarity)
- **AI Model**: Gemini API (`gemini-1.5-flash`)
- **Frontend**: React (Vite), plain CSS

## Prompt Design Notes
The Gemini system instruction was iteratively designed to ensure strict adherence to the context:
- *Initial iteration*: A naive prompt might allow the model to hallucinate or pull from external knowledge.
- *Current iteration*: The prompt explicitly instructs the AI: "You are a helpful assistant that answers questions based ONLY on the provided document context. If the answer is not contained in the text, you must say exactly: 'I could not find that in the document'. Do not make up information. Keep your answer brief, about 3-4 sentences maximum." This successfully constrains the model's output and keeps it concise.

## Setup Instructions

### Backend Setup
1. Open a terminal and navigate to the `backend` directory.
2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your Gemini API key as an environment variable:
   ```bash
   # On Windows PowerShell
   $env:GEMINI_API_KEY="your-api-key-here"
   # On Mac/Linux
   export GEMINI_API_KEY="your-api-key-here"
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`.

### Frontend Setup
1. Open a new terminal and navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open the displayed local URL in your browser (usually `http://localhost:5173`).

## Known Limitations
- **In-Memory Storage**: The extracted PDF text and embeddings are stored in memory and will be lost if the server restarts.
- **Single User/Document**: The current implementation holds state globally in the backend, meaning only one PDF can be active at a time for all users. Uploading a new PDF will overwrite the previous one.
- **No Authentication**: There is no user login or API key protection on the endpoints.
- **Basic Similarity Search**: It uses a simple O(N) numpy cosine similarity scan instead of a dedicated, optimized vector database (like Pinecone or ChromaDB).

<!-- Added for profile activity update -->
