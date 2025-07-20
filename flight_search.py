import dotenv
import os
import requests

AMADEUS_ENDPOINT = "https://test.api.amadeus.com"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        dotenv.load_dotenv()
        self.amadeus_api_key = os.getenv("AMADEUS_API_KEY")
        self.amadeus_api_secret = os.getenv("AMADEUS_API_SECRET")
        self.headers = {
            "Authorization": f"Bearer {self.amadeus_api_key}"
        }

    def search_flights(self):
        response = requests.get(url=f"{AMADEUS_ENDPOINT}/v1/shopping/flight-destinations?origin=PAR&maxPrice=200"
                                    ,headers=self.headers)
        response.raise_for_status()
        return response.json()

search = FlightSearch()
search.search_flights()