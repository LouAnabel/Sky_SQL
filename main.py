import sqlalchemy
from datetime import datetime
from typing import Callable, Dict, Any, List, Tuple

DATABASE_CONNECTION_STRING = 'sqlite:///data/flights.sqlite3'
AIRPORT_CODE_LENGTH = 3


def query_delayed_flights_by_carrier(data_handler):
    """Query and display delayed flights for a specific airline."""
    carrier_name = input("Enter airline name: ")
    flight_results = data_handler.get_delayed_flights_by_airline(carrier_name)
    display_flight_results(flight_results)


def query_delayed_flights_by_origin(data_handler):
    """Query and display delayed flights from a specific airport."""
    while True:
        origin_code = input("Enter origin airport IATA code: ")
        if origin_code.isalpha() and len(origin_code) == AIRPORT_CODE_LENGTH:
            break
        print("Invalid airport code. Please try again.")

    flight_results = data_handler.get_delayed_flights_by_airport(origin_code)
    display_flight_results(flight_results)


def query_flight_by_identifier(data_handler):
    """Query and display a flight by its unique identifier."""
    while True:
        try:
            flight_id = int(input("Enter flight ID: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric ID.")

    flight_results = data_handler.get_flight_by_id(flight_id)
    display_flight_results(flight_results)


def query_flights_by_travel_date(data_handler):
    """Query and display flights for a specific date."""

    while True:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            travel_date = datetime.strptime(date_input, '%d/%m/%Y')
            break
        except ValueError as error:
            print(f"Invalid date format. {error}")

    flight_results = data_handler.get_flights_by_date(travel_date.day, travel_date.month, travel_date.year)
    display_flight_results(flight_results)


def display_flight_results(flight_results: List[Any]):
    """Display flight results with appropriate formatting."""
    print(f"Got {len(flight_results)} results.")

    for result in flight_results:
        result_dict = result._mapping

        try:
            flight_delay = int(result_dict.get('DELAY', 0))
            origin_airport = result_dict['ORIGIN_AIRPORT']
            destination_airport = result_dict['DESTINATION_AIRPORT']
            carrier = result_dict['AIRLINE']
            flight_id = result_dict['ID']
        except (ValueError, KeyError, sqlalchemy.exc.SQLAlchemyError) as error:
            print(f"Error processing result: {error}")
            continue

        # Different output for delayed and non-delayed flights
        if flight_delay > 0:
            print(f"{flight_id}. {origin_airport} -> {destination_airport} by {carrier}, Delay: {flight_delay} Minutes")
        else:
            print(f"{flight_id}. {origin_airport} -> {destination_airport} by {carrier}")


def show_application_menu() -> Callable:
    """Display the application menu and get user's menu choice.
    Returns: Callable: Function corresponding to user's menu selection."""

    menu_options: Dict[int, Tuple[Callable, str]] = {
        1: (query_flight_by_identifier, "Show flight by ID"),
        2: (query_flights_by_travel_date, "Show flights by date"),
        3: (query_delayed_flights_by_carrier, "Delayed flights by airline"),
        4: (query_delayed_flights_by_origin, "Delayed flights by origin airport"),
        5: (quit, "Exit")
    }

    print("\n------Menu------\n")
    for key, (_, description) in menu_options.items():
        print(f"{key}. {description}")

    while True:
        try:
            user_choice = int(input("\nPlease enter your choice (1-5): "))
            if user_choice in menu_options:
                return menu_options[user_choice][0]
        except ValueError:
            pass
        print("Invalid selection. Try again...")


def main():
    """Main application entry point."""
    from data import FlightData  # Local import to avoid circular dependency

    data_manager = FlightData(DATABASE_CONNECTION_STRING)

    while True:
        selected_function = show_application_menu()
        selected_function(data_manager)


if __name__ == "__main__":
    main()