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
        self.endpoint = os.getenv("AMADEUS_ENDPOINT")
        self.token = self._get_new_token()
        self.tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        self.six_month_from_today = (datetime.date.today() + datetime.timedelta(days=(6 * 30))).isoformat()

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
        response.raise_for_status()  # <-- Para detectar errores de inmediato

        data = response.json()
        token = data.get("access_token")

        if not token:
            raise ValueError(f"⚠️ Could not fetch token. Response: {data}")

        print(f"✅ Token generated successfully. Expires in {data.get('expires_in', 'unknown')} seconds")
        return token

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
                "max": 1,
                "returnDate": self.six_month_from_today
            }
        )
        response.raise_for_status()

        data = response.json()
        try:
            return data
        except (IndexError, KeyError):
            print(f"⚠️ No flight offers found. Full response: {data}")
            return None



