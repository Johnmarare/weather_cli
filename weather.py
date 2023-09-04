#!/usr/bin/python3
# weather.py


import sys
import argparse
import json
from configparser import ConfigParser
from urllib import parse, request, error

import style

# Constants
BASE_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)


# Let us Read User CLI Arguments
def read_user_cli_args():
    """Handles the CLI user interactions

    Returns:
        argparse.Namespace: Populated namespace object
    """
    parser = argparse.ArgumentParser(
        description="gets weather and temprature information of a city. "
    )
    parser.add_argument(
        'city',
        nargs='+',
        type=str,
        help="enter the city name"
    )
    parser.add_argument(
        '-i',
        '--imperial',
        action='store_true',
        help='display the temprature in imperial units',
    )
    args = (parser.parse_args())

    if not args.city:
        sys.exit("Please provide the name of a city.")

    return (args)


# Build Weather Query URL
def build_weather_query(city_input, imperial=False):
    """Builds the URL for an API request to Openweather API.

    Args:
        city_input (list[]): Name of a city as collected by argparse
        imperial (bool): Whether or not to use imperial units for temprature.

    Returns:
        str: URL formatted for a call to openWeather's city name endpoint.
    """
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = 'imperial' if imperial else 'metric'
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return (url)


# Now we Get API key from configuration   
def _get_api_key():
    """Fetch API key from configuration file.
    Expects a configuration file named "secrets.ini"
    """
    try:
        config = ConfigParser()
        config.read("secrets.ini")
        api_key = config["openweather"]["api_key"]
    except FileNotFoundError:
        sys.exit("Configuration file not found.")
    except (KeyError, ConfigParser.NoSectionError):
        sys.exit("Invalid or missing API key in the configuration file.")

    return (api_key)


# Here, We Get Weather Data from API
def get_weather_data(query_url):
    """Makes an API request to a URL and returns the data as a python object.

    Args:
        query_url (str): URL formatted for openweather city name endpoint.

    Returns:
        dict: Weather information for a specific city.
    """
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 404: # Location not found
            sys.exit("Can't find weather data for this Location.")
        elif http_error.code == 401: # Unauthorized. API error.
            sys.exit("Access denied. Check your API key.")
        else:
            sys.exit("something went wrong... ({})".format(http_error))
    
    data = response.read()

    try:
        return (json.loads(data))

    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")
    

# We have the Data, Let us Display the Weather Information.
def display_weather_info(weather_data, imperial=False):
    """Prints formatted weather information about a Location.

    Args:
        weather_data (dict): API response fom Openweather.
        imperial (bool): Whether or not to use imperial units.
    """
    city = weather_data["name"]
    weather_id = weather_data["weather"][0]["id"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]

    style.change_color(style.REVERSE)
    print(f"{city:^{style.PADDING}}", end="")
    style.change_color(style.RESET)

    weather_symbol, color = _select_weather_display_params(weather_id)

    style.change_color(color)
    print(f"\t{weather_symbol}", end=" ")
    print(
        f"\t{weather_description.capitalize():^{style.PADDING}}",
        end=" "
    )
    style.change_color(style.RESET)

    print(f"({temperature}°{'F' if imperial else 'C'})")


# Select Weather Display Parameters.
def _select_weather_display_params(weather_id):
    if weather_id in THUNDERSTORM:
        display_params = ("💥", style.RED)
    elif weather_id in DRIZZLE:
        display_params = ("💧", style.CYAN)
    elif weather_id in RAIN:
        display_params = ("💦", style.BLUE)
    elif weather_id in SNOW:
        display_params = ("⛄️", style.WHITE)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀", style.BLUE)
    elif weather_id in CLEAR:
        display_params = ("🔆", style.YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("💨", style.PURPLE)
    else:  # In case the API adds new weather codes
        display_params = ("🌈", style.RESET)
    return (display_params)


if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city, user_args.imperial)
    weather_data = get_weather_data(query_url)
    display_weather_info(weather_data, user_args.imperial)

