```python
import unittest
import requests

class TestTicketClassifier(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:5000'
    
    def test_classify_ticket(self):
        response = requests.post(f'{self.base_url}/classify', json={
            "ticket_text": "Customer requested a refund after receiving incorrect product."
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['tickets'][0]['category'], 'customer_support')
    
    def test_get_classified_tickets(self):
        response = requests.get(f'{self.base_url}/classified-tickets')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
    
    def test_delete_unclassified_tickets(self):
        response = requests.delete(f'{self.base_url}/unclassified-tickets')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

if __name__ == '__main__':
    unittest.main()
```