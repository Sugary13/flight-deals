import os
import dotenv
import requests

class DataManager:
    """This class is responsible for talking to the Google Sheet."""

    def __init__(self):
        dotenv.load_dotenv()
        self.sheety_endpoint = os.getenv("SHEETY_ENDPOINT")  # <- URL del endpoint
        self.sheety_token = os.getenv("BEARER_TOKEN")        # <- Bearer token real
        self.headers = {
            "Authorization": f"Bearer {self.sheety_token}"
        }

    def get_data(self):
        response = requests.get(url=self.sheety_endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post_data(self, data):
        response = requests.post(url=self.sheety_endpoint, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def put_data(self, data, object_id):
        response = requests.put(url=f"{self.sheety_endpoint}/{object_id}", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete_data(self, object_id):
        response = requests.delete(f"{self.sheety_endpoint}/{object_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()
