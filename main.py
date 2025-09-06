import time
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()


for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # slowing down requests to avoid rate limit
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()



destinations = data_manager.get_destination_data()

for city in destinations:
    iata_code = city["iataCode"]

    flight_offer = flight_search.find_cheapest_price(iata_code)

    if flight_offer:
        flight_data = FlightData()
        formatted = flight_data.flight_data(flight_offer)
        print(formatted)
