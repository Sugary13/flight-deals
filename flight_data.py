from flight_search import FlightSearch



flightSearch = FlightSearch()

class FlightData:
    #This class is responsible for structuring the flight data.

    def __init__(self):
        self.price = "N/A"
        self.origin_airport = "N/A"
        self.destination_airport = "N/A"
        self.out_date = "N/A"
        self.return_date = "N/A"



    def flight_data(self, data):
        try:
            self.price = data["data"][0]["price"]["total"]
            self.origin_airport = data["data"][0]["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            self.destination_airport = data["data"][0]["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            self.out_date = data["data"][0]["itineraries"][0]["segments"][0]["departure"]["at"]
            self.return_date = data["data"][0]["itineraries"][1]["segments"][0]["arrival"]["at"]

            structured_data = {
                "Price": self.price,
                "OriginAirport": self.origin_airport,
                "DestinationAirport": self.destination_airport,
                "Out-Date": self.out_date.split("T")[0],
                "Return-Date": self.return_date.split("T")[0],
            }

            return structured_data

        except (KeyError, IndexError) as e:
            print(f"⚠️ Error extracting flight data: {e}")
            return {
                "Price": "N/A",
                "OriginAirport": "N/A",
                "DestinationAirport": "N/A",
                "Out-Date": "N/A",
                "Return-Date": "N/A",
            }
