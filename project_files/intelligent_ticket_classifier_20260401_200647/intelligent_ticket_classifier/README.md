# Intelligent Ticket Classifier

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 14+

### Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/intelligent_ticket_classifier.git
cd intelligent_ticket_classifier
```

2. Set up environment variables
```bash
cp .env.example .env
```

3. Install backend dependencies
```bash
pip install -r requirements.txt
```

4. Initialize database
```bash
python src/db_init.py
```

5. Start backend server
```bash
python src/main.py
```

6. Start frontend development server
```bash
cd frontend
npm install
npm start
```

## API Endpoints
- POST /classify
- GET /classified-tickets
- DELETE /unclassified-tickets

## Features
- Rule-based ticket classification
- Machine learning model integration
- PostgreSQL database
- React.js frontend
- Error handling and logging

## Configuration
- Database settings in `config/db_config.py`
- ML model settings in `config/ml_config.py`

---