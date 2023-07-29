# -*- coding: utf-8 -*-
import requests
import api_config
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


def get_data(LANGUAGE):
    """
    This function prompts the user to enter the name of the city 
    to be queried. It builds a URL with the provided city, API key,
    and language, and makes a request to the OpenWeatherMap API 
    to get weather data for the specified city.

    Args:
        LANGUAGE (str): The language code for the desired language 
        of the weather data.

    Returns:
        data (dict): A dictionary containing the weather data for
        the specified city.
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
    This function takes weather data as input and prints the current 
    weather information for today, including the weather description, 
    temperature (current, minimum, and maximum), and humidity for the 
    specified city.

    Args:
        data (dict): A dictionary containing the weather data for the 
        specified city.

    Returns:
        None
    """
    weather = data["weather"][0]["description"]
    temp_min = data["main"]["temp_min"]
    temp = data["main"]["temp"]
    temp_max = data["main"]["temp_max"]
    humidity = data["main"]["humidity"]
    city = data["name"]

    print(TRANSLATIONS["today_head"].format(city))
    print(TRANSLATIONS["today_weather"].format(weather))
    print(TRANSLATIONS["today_temp"].format(temp))
    print(TRANSLATIONS["today_min"].format(temp_min))
    print(TRANSLATIONS["today_max"].format(temp_max))
    print(TRANSLATIONS["today_humidity"].format(humidity))


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
        option = get_and_validate_option(4)
        if option == 4: # Exit
            break
        elif option == 1: # Get today's weather
            get_weather_today(data)
        elif option == 2:  # TODO
            print("")
        elif option == 3: # Change city
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