```python
import dill
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB

# Load pre-trained model (in production, this would be loaded from a file)
def load_model():
    try:
        with open('models/ticket_classifier.pkl', 'rb') as f:
            model = dill.load(f)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}")

# Simple rule-based classifier (for demonstration)
def rule_based_classifier(text):
    if "refund" in text.lower() or "return" in text.lower():
        return "customer_support"
    if "payment" in text.lower() or "billing" in text.lower():
        return "billing_issues"
    if "product" in text.lower() or "feature" in text.lower():
        return "product_inquiries"
    return "uncategorized"

# Main classification function
def classify_ticket(text):
    try:
        # In production, use the ML model
        model = load_model()
        prediction = model.predict([text])[0]
        return prediction
    except Exception as e:
        # Fallback to rule-based classifier if ML model fails
        return rule_based_classifier(text)
```

---