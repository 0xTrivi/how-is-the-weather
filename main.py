# -*- coding: utf-8 -*-
import requests
import api_config
import datetime
import pytz
API_KEY=api_config.api_key 
URL=api_config.url

global TRANSLATIONS
global LANGUAGE


def check_range(option, max_range):
    """
    This function validates if the received integer is within the range
    of options (between 1 and the specified maximum).
    """
    return 1 <= option <= max_range


def get_and_validate_option(max_option):
    """
    This function validates if the value entered by the user is valid
    (being an integer and within the range of options). 
    It takes the maximum value of the option range as input and returns
    the valid integer entered by the user.

    Args:
        max_option (int): Maximum number of the option range.
    Returns:
        option (int): Valid integer entered by the user.
    """
    while True:
        try:
            option = int(input())
            if check_range(option,max_option):
                return option
            else:
                print("Please, select a correct option.")
        except ValueError:
            print("Please, enter the correct data type (int).")


def load_translations(LANGUAGE):
    """
    This function receives a language code and returns a dictionary
    to be able to print the program's texts in the indicated language.

    Args:
        LANGUAGE (str): Code of the required language
    Returns:
        TRANSLATIONS (dict): Dictionary with the texts in the required language.
    """
    TRANSLATIONS = {}
    file_name = "languages/texts_" + LANGUAGE + ".txt"
    try:
        with open(file_name, "r", encoding = "utf-8") as file:
            for line in file:
                key, value = line.strip().split("=")
                TRANSLATIONS[key] = value
    except FileNotFoundError:
        print("Error, {} file not found.".format(file_name))
        raise

    return TRANSLATIONS


def select_language():
    """
    This function displays to the user the available languages and 
    allows them to select one by entering the corresponding option.
    It returns the code of the selected language.

    Returns:
        LANGUAGE (str): Code of the selected language.
    """
    print("")
    print("Select a lenguage and press enter: ")
    print("1 - English")
    print("2 - Español")
    
    language_select = get_and_validate_option(2)
    print("")
    if(language_select == 2):
        LANGUAGE = "es"
    else:
        LANGUAGE = "en"
    
    return LANGUAGE


def select_city():
    """
    This function prompts the user to enter the name of the city
    to be queried. It returns the validated string.

    Returns:
        city (str): Name of the entered city.
    """
    while True:
        print(TRANSLATIONS["select_city"])
        city = input()
        if city.strip():
            return city
        else:
            print(TRANSLATIONS["error"])


def transform_ts_to_local_time(timestamp):
    """
    Converts the provided timestamp to local time in the 'Europe/Madrid' timezone.
    
    Args:
        timestamp (int): The timestamp to be converted to local time.

    Returns:
        str: A string representing the local time in the format 'HH:MM'.
    """
    ts_to_local_date_utc = datetime.datetime.fromtimestamp(timestamp, tz=pytz.utc)
    time_zone = pytz.timezone('Europe/Madrid')
    local_date_hour = ts_to_local_date_utc.astimezone(time_zone)
    hour_local = local_date_hour.strftime('%H:%M')

    return hour_local


def get_data(LANGUAGE):
    """
    This function prompts the user to enter the name of a city through 
    'select_city()' function, and then makes a request to the OpenWeatherMap API 
    to fetch the weather forecast for the specified city.
    The weather data is returned as a dictionary.

    Args:
        LANGUAGE (str): Code of the selected language.

    Returns:
        data (dict): A dictionary containing weather forecast data for 
        the selected city.
    """
    while True:
        city=select_city()
        
        url = "{}?q={}&appid={}&units=metric&lang={}".format(
            URL, city, API_KEY, LANGUAGE)
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful.
            data = response.json() # Convert to dictionary
            return data
        except requests.exceptions.RequestException as e:
            print(TRANSLATIONS["api_error"].format(e))


def get_weather_today(data):
    """
    The function extracts the current weather data for today from the 'data' dictionary,

    Args:
        data (dict): A dictionary containing weather forecast data

    Returns:
        None
    """
    now_data = data["list"][0]
    
    weather = now_data["weather"][0]["description"]
    temp = now_data["main"]["temp"]
    humidity = now_data["main"]["humidity"]
    city = data["city"]["name"]
    print("")
    print(TRANSLATIONS["now_head"].format(city))
    print(TRANSLATIONS["weather"].format(weather))
    print(TRANSLATIONS["temp"].format(temp))
    print(TRANSLATIONS["humidity"].format(humidity))


def get_forescat(data):
    """
    This function extracts weather forecasts for multiple hours of the next 5 days.

    Args:
        data (dict): A dictionary containing weather forecast data

    Returns:
        None
    """
    forescat_days = data["list"]  
    print("")
    for forecast in forescat_days:
        date = forecast["dt_txt"]
        weather = forecast["weather"][0]["description"]
        humidity = forecast["main"]["humidity"]
        temp = forecast["main"]["temp"]
        print("")
        print(TRANSLATIONS["date"].format(date))
        print(TRANSLATIONS["weather"].format(weather))
        print(TRANSLATIONS["temp"].format(temp))
        print(TRANSLATIONS["humidity"].format(humidity))


def get_data_sun(data):
    """
    Retrieves sunrise and sunset timestamps from the provided data 
    dictionary and converts them to local time using the 'transform_ts_to_local_time'.

    Args:
        data (dict):A dictionary containing the weather data for the 
        specified city.

    Returns:
        None
    """
    ts_sunrise = data["city"]["sunrise"]
    ts_sunset = data["city"]["sunset"]

    sunrise_hour = transform_ts_to_local_time(ts_sunrise)
    sunset_hour = transform_ts_to_local_time(ts_sunset)
    print("")
    print(TRANSLATIONS["sun"].format(sunrise_hour, sunset_hour)) 


def menu():
    """
    This function displays a menu to the user and allows them to select 
    various options. It calls the 'get_data' function to retrieve weather 
    data for the specified city, and then enters a loop to repeatedly 
    display the menu and process user input until the user chooses to 
    exit the program.

    Returns:
        None
    """
    data=get_data(LANGUAGE)

    while True:
        print("")
        print(TRANSLATIONS["menu_0"])
        print(TRANSLATIONS["menu_1"])
        print(TRANSLATIONS["menu_2"])
        print(TRANSLATIONS["menu_3"])
        print(TRANSLATIONS["menu_4"])
        print(TRANSLATIONS["menu_5"])
        option = get_and_validate_option(5)
        if option == 5: # Exit
            break
        elif option == 1: # Get the current weather
            get_weather_today(data)
        elif option == 2:  # Display the sunrise and sunset time for today
            get_data_sun(data)
        elif option == 3: # Show the forecast for the next 5 days
            get_forescat(data)
        elif option == 4: # Change the city
            data=get_data(LANGUAGE)


if __name__ == '__main__':
    """
    The main entry point of the program.
    It allows the user to select the language and loads translations 
    accordingly. The 'menu' function is then called to display 
    options and process user input.
    """
    LANGUAGE = select_language()

    TRANSLATIONS = load_translations(LANGUAGE)

    menu()