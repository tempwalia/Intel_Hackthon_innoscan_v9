```python
from src import db
from src.models import Ticket

def init_db():
    try:
        with db.create_all():
            pass
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization failed: {str(e)}")
```

---