import { useState } from 'react'
import './index.css'

const BACKEND_URL = 'http://localhost:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState([])
  const [isUploading, setIsUploading] = useState(false)
  const [isAsking, setIsAsking] = useState(false)
  const [uploadMessage, setUploadMessage] = useState('')

  // Handle file selection
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
      setUploadMessage('')
    }
  }

  // Handle PDF upload
  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadMessage('Please select a PDF file first.')
      return
    }

    setIsUploading(true)
    setUploadMessage('')

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await fetch(`${BACKEND_URL}/upload`, {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      
      if (data.error) {
        setUploadMessage(`Error: ${data.error}`)
      } else {
        setUploadMessage(data.message || 'Upload successful!')
      }
    } catch (error) {
      setUploadMessage(`Failed to upload: ${error.message}`)
    } finally {
      setIsUploading(false)
    }
  }

  // Handle asking a question
  const handleAsk = async () => {
    if (!question.trim()) {
      return
    }

    setIsAsking(true)
    setAnswer('')
    setSources([])

    try {
      const response = await fetch(`${BACKEND_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })
      const data = await response.json()

      if (data.error) {
        setAnswer(`Error: ${data.error}`)
      } else {
        setAnswer(data.answer)
        setSources(data.sources || [])
      }
    } catch (error) {
      setAnswer(`Failed to ask question: ${error.message}`)
    } finally {
      setIsAsking(false)
    }
  }

  return (
    <div className="app-container">
      <header className="header">
        <h1>AI PDF Q&A Tool</h1>
        <p className="subtitle">Upload a PDF and ask questions to get AI-generated answers directly from the text.</p>
      </header>

      <main className="main-content">
        {/* Section 1: Upload PDF */}
        <section className="card upload-section">
          <h2>1. Upload Document</h2>
          <div className="input-group">
            <input 
              type="file" 
              accept=".pdf" 
              onChange={handleFileChange} 
              className="file-input" 
              id="file-upload"
            />
            <label htmlFor="file-upload" className="file-label">
              {selectedFile ? selectedFile.name : 'Choose a PDF file...'}
            </label>
            <button 
              onClick={handleUpload} 
              disabled={isUploading || !selectedFile}
              className="btn btn-primary"
            >
              {isUploading ? 'Uploading...' : 'Upload PDF'}
            </button>
          </div>
          {uploadMessage && <p className="status-message">{uploadMessage}</p>}
        </section>

        {/* Section 2: Ask Question */}
        <section className="card ask-section">
          <h2>2. Ask a Question</h2>
          <div className="input-group column">
            <textarea 
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="What is this document about?"
              className="text-input"
              rows={3}
            />
            <button 
              onClick={handleAsk} 
              disabled={isAsking || !question.trim()}
              className="btn btn-secondary"
            >
              {isAsking ? 'Thinking...' : 'Ask AI'}
            </button>
          </div>
        </section>

        {/* Section 3: Answer & Sources */}
        {(answer || isAsking) && (
          <section className="card result-section">
            <h2>3. Answer</h2>
            {isAsking ? (
              <div className="loading-spinner"></div>
            ) : (
              <div className="answer-box">
                <p className="answer-text">{answer}</p>
                
                {sources.length > 0 && (
                  <div className="sources-container">
                    <h3>Sources used:</h3>
                    <ul className="source-list">
                      {sources.map((source, idx) => (
                        <li key={idx} className="source-item">
                          "{source.length > 200 ? source.substring(0, 200) + '...' : source}"
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  )
}

export default App
