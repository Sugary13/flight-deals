import dotenv
import os
import requests
import datetime

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        dotenv.load_dotenv()
        self.amadeus_api_key = os.getenv("AMADEUS_API_KEY")
        self.amadeus_api_secret = os.getenv("AMADEUS_API_SECRET")
        self.token = self._get_new_token()
        self.tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.endpoint = os.getenv("AMADEUS_ENDPOINT")
        self.tomorrow = self.tomorrow.isoformat()

    def _get_new_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self.amadeus_api_key,
            "client_secret": self.amadeus_api_secret,
        }
        response = requests.post(f"{self.endpoint}/v1/security/oauth2/token", headers=header, data=body)
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()["access_token"]

    def get_destination_code(self, city):
        response = requests.get(
            url=f"{self.endpoint}/v1/reference-data/locations/cities",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.amadeus+json"
            },
            params={
                "keyword": city.title(),
                "subType": "CITY,AIRPORT"
            }
        )
        response.raise_for_status()

        try:
            return response.json()["data"][0]["iataCode"]
        except (IndexError, KeyError):
            print(f"⚠️ No IATA code found for {city}. Full response: {response.json()}")
            return None

    def find_cheapest_price(self, destination_code):
        response = requests.get(
            url=f"{self.endpoint}/v2/shopping/flight-offers",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.amadeus+json"
            },
            params={
                "originLocationCode": "LON",
                "destinationLocationCode": destination_code,
                "departureDate": self.tomorrow,
                "adults": 1,
                "currencyCode": "GBP",
                "max": 1
            }
        )
        response.raise_for_status()

        data = response.json()
        try:
            return data["data"][0]
        except (IndexError, KeyError):
            print(f"⚠️ No flight offers found. Full response: {data}")
            return None
