```python
import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import db_config
from models import Ticket
from ml_classifier import classify_ticket

app = Flask(__name__)
app.config.from_object(db_config)
db = SQLAlchemy(app)

# Initialize database
with app.app_context():
    db.create_all()

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/classify', methods=['POST'])
def classify():
    try:
        data = request.get_json()
        if not data or 'ticket_text' not in data:
            return jsonify({"status": "error", "message": "Missing ticket text"}), 400
        
        ticket_text = data['ticket_text']
        category = classify_ticket(ticket_text)
        
        new_ticket = Ticket(text=ticket_text, category=category)
        db.session.add(new_ticket)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "tickets": [{"ticket_id": new_ticket.id, "category": category, "text": ticket_text}]
        }), 200
    
    except Exception as e:
        logging.error(f"Classification error: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/classified-tickets', methods=['GET'])
def get_classified_tickets():
    try:
        tickets = Ticket.query.all()
        return jsonify({
            "status": "success",
            "tickets": [{"ticket_id": t.id, "category": t.category, "text": t.text} for t in tickets]
        }), 200
    
    except Exception as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/unclassified-tickets', methods=['DELETE'])
def mark_unclassified():
    try:
        # In a real implementation, this would mark tickets as unclassified
        # For this demo, we'll just return a success response
        return jsonify({"status": "success", "message": "Tickets marked as unclassified"}), 200
    
    except Exception as e:
        logging.error(f"Error marking tickets: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

---