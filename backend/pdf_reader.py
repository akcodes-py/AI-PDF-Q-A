import pdfplumber

def get_text_from_pdf(pdf_file_path):
    """
    Extracts all text from a given PDF file using pdfplumber.
    """
    full_text = ""
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return full_text

def split_text_into_chunks(full_text, chunk_size=500):
    """
    Splits a large string of text into smaller chunks of about 'chunk_size' words.
    """
    words = full_text.split()
    chunks = []
    
    # Loop through the words, creating chunks of 'chunk_size'
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        
    return chunks
