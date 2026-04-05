```javascript
import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [ticketText, setTicketText] = useState('');
  const [classificationResult, setClassificationResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setClassificationResult(null);
    
    try {
      const response = await axios.post('http://localhost:5000/classify', {
        ticket_text: ticketText
      });
      
      setClassificationResult(response.data);
    } catch (err) {
      setError('Failed to classify ticket. Please try again.');
      console.error(err);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Intelligent Ticket Classifier</h1>
      </header>
      <main className="container mt-5">
        <div className="card">
          <div className="card-body">
            <h2 className="card-title">Classify Ticket</h2>
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="ticketText" className="form-label">Ticket Text</label>
                <textarea
                  id="ticketText"
                  className="form-control"
                  rows="5"
                  value={ticketText}
                  onChange={(e) => setTicketText(e.target.value)}
                  required
                ></textarea>
              </div>
              <button type="submit" className="btn btn-primary">Classify</button>
            </form>
            {error && <div className="alert alert-danger mt-3">{error}</div>}
            {classificationResult && (
              <div className="mt-4">
                <h3>Classification Result</h3>
                <p><strong>Category:</strong> {classificationResult.tickets[0].category}</p>
                <p><strong>Ticket Text:</strong> {classificationResult.tickets[0].text}</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
```

---