from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


QUERY_FLIGHT_BY_ID = ("SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, "
                      "flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines "
                      "ON flights.airline = airlines.id WHERE flights.ID = :id")

QUERY_FLIGHT_BY_DATE = ("SELECT id AS ID, origin_airport AS ORIGIN_AIRPORT, destination_airport "
                        "AS DESTINATION_AIRPORT, departure_delay AS DELAY, AIRLINE "
                        "FROM flights WHERE day = :day AND month = :month AND year = :year "
                        "ORDER BY DELAY DESC")

QUERY_DELAYED_FLIGHT_BY_AIRLINE = ("SELECT f.id AS ID, f.origin_airport AS ORIGIN_AIRPORT, "
                                   "f.destination_airport AS DESTINATION_AIRPORT, "
                                   "f.departure_delay AS DELAY, ""a.airline AS AIRLINE "
                                   "FROM flights as f JOIN airlines as a ON f.airline = a.id "
                                   "WHERE a.airline = :airline_name AND DELAY >= 20")

QUERY_DELAYED_FLY_BY_AIRPORT = ("SELECT f.id AS ID, f.origin_airport AS ORIGIN_AIRPORT, "
                                "f.destination_airport AS DESTINATION_AIRPORT, "
                                "f.departure_delay AS DELAY, a.airline AS AIRLINE "
                                "FROM flights as f JOIN airlines as a ON f.airline = a.id "
                                "WHERE ORIGIN_AIRPORT = :airport_code AND DELAY  >= 20 ")

class FlightData:
    """
    The FlightData class is a Data Access Layer (DAL) object that provides an
    interface to the flight data in the SQLITE database. When the object is created,
    the class forms connection to the sqlite database file, which remains active
    until the object is destroyed.
    """
    def __init__(self, db_uri):
        """
        Initialize a new engine using the given database URI
        """
        self._engine = create_engine(db_uri)


    def _execute_query(self, query, params):
        """
        Execute an SQL query with the params provided in a dictionary,
        and returns a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.
        """
        try:
            with self._engine.connect() as connection:
                results = connection.execute(text(query), params)
                return results.fetchall()
        except SQLAlchemyError as e:  # Catch SQLAlchemy-specific errors
            print(f"Database error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []


    def get_flight_by_id(self, flight_id):
        """
        Searches for flight details using flight ID.
        If the flight was found, returns a list with a single record.
        """
        params = {'id': flight_id}
        return self._execute_query(QUERY_FLIGHT_BY_ID, params)


    def get_flights_by_date(self, day, month, year):
        """
        Searches for flight details using flight date.
        If the flight was found, returns a list with all the
        flights in this date.
        """
        params = {"day" : day, "month" : month, "year" : year}
        return self._execute_query(QUERY_FLIGHT_BY_DATE, params)


    def get_delayed_flights_by_airline(self, airline_input):
        """
        Searches for delayed flights details using airline name.
        If the flight was found, returns a list with all the
        flights in this airline name.
        """
        params = {"airline_name" : f"{airline_input}"}
        return self._execute_query(QUERY_DELAYED_FLIGHT_BY_AIRLINE, params)


    def get_delayed_flights_by_airport(self, airport_input):
        """
        Searches for delayed flights details using iata_code.
        If the flight was found, returns a list with all the
        flights in this iata_code.
        """
        params = {"airport_code": airport_input}
        return self._execute_query(QUERY_DELAYED_FLY_BY_AIRPORT, params)


    def __del__(self):
        """
        Closes the connection to the databse when the object is about to be destroyed
        """
        self._engine.dispose()