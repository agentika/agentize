from __future__ import annotations

from typing import Literal

from agents import function_tool
from fast_flights import FlightData
from fast_flights import Passengers
from fast_flights import Result
from fast_flights import create_filter
from fast_flights import get_flights_from_filter


def get_flights(
    depart_date: str,
    from_airport: str,
    to_airport: str,
    seat: Literal["economy", "premium-economy", "business", "first"] = "economy",
    adults: int = 1,
) -> Result:
    """Query the flight

    Args:
        depart_date (str): Beginning trip date (YYYY-MM-DD)
        from_airport (str): Where from? Departure (airport) IATA 3-letter Location Code.
        to_airport (str): Where to? Arrival (airport) IATA 3-letter Location Code.
        seat (str): Seat class. only ["economy", "premium-economy", "business", "first"].
        adults (int): Number of adults.
        children (int): Number of children.

    Returns:
        results (Result): Flight search results.
    """

    filter = create_filter(
        flight_data=[
            FlightData(date=depart_date, from_airport=from_airport, to_airport=to_airport),
        ],
        trip="one-way",
        seat=seat,
        passengers=Passengers(adults=adults, children=0, infants_in_seat=0, infants_on_lap=0),
        max_stops=0,
    )

    result = get_flights_from_filter(filter, mode="common")
    return result


get_flights_tool = function_tool(get_flights)
