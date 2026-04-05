```python
from datetime import datetime
from src import db

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ticket {self.id}>'
```

---