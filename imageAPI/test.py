import json
from rest_framework import status
from rest_framework.test import APIClient

client = APIClient()

user_1_password = "testPassword123"
user_1_username = "testUser"


def get_token(username, password):
    data = {
        'username': username,
        'password': password,
    }
    response = client.post('/token/', data=json.dumps(data), content_type='application/json')
    if response.status_code == status.HTTP_200_OK:
        return json.loads(response.content).get('access')
    else:
        return None
