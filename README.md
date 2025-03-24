# Flight Data Analysis Application

## Project Overview

This Flight Data Analysis Application is a Python-based tool for querying and analyzing flight data stored in a SQLite database. The application provides a flexible interface to retrieve flight information based on various criteria such as flight ID, date, airline, and airport.

## Features

- Query flights by unique identifier
- Retrieve flights for a specific date
- Find delayed flights by airline
- Identify delayed flights from a specific airport
- Minimal dependencies and easy to integrate

## Prerequisites

- Python 3.8+
- SQLite database with flight data

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flight-data-analysis.git
   cd flight-data-analysis
   
# Usage Examples
## Basic Queries

+ from src.flight_data import FlightData

# Open database connection
with FlightData('data/flights.sqlite3') as flight_data:
    
    # Get flight by ID
    flight = flight_data.get_flight_by_id(123)
    
    # Get flights on a specific date
    date_flights = flight_data.get_flights_by_date(15, 3, 2024)
    
    # Find delayed flights for an airline
    delayed_flights = flight_data.get_delayed_flights_by_airline('Delta')
    
    # Find delayed flights from an airport
    airport_delays = flight_data.get_delayed_flights_by_airport('LAX')
