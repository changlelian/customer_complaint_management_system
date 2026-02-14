import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client

c = Client()
try:
    response = c.post('/api/login/', {'username': 'admin', 'password': 'admin123'}, content_type='application/json')
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"Content: {response.content.decode()[:500]}...") # Print first 500 chars
    else:
        print(f"Token: {response.json()}")
except Exception as e:
    print(f"Exception: {e}")
