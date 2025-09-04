import os
import dotenv
import requests

class DataManager:
    """This class is responsible for talking to the Google Sheet."""

    def __init__(self):
        dotenv.load_dotenv()
        self.sheety_endpoint = os.getenv("SHEETY_ENDPOINT")
        self.sheety_token = os.getenv("BEARER_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.sheety_token}"
        }
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.sheety_endpoint, headers=self.headers)
        response.raise_for_status()
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            if not city["iataCode"]:
                print(f"⚠️ Skipping {city['city']} (no IATA code yet)")
                continue

            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self.sheety_endpoint}/{city['id']}",
                json=new_data,
                headers=self.headers
            )
            response.raise_for_status()
            print(f"✅ Updated {city['city']} → {city['iataCode']}")

