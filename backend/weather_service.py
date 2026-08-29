import requests


def get_city_coordinates(city):
    
    # Open-Meteo Geocoding API
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"


    # Information we are sending to the API
    parameters = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }


    # Send request to the Geocoding API
    response = requests.get(geocoding_url, params=parameters)


    # Convert JSON response into a Python dictionary
    city_data = response.json()


    # Check if the city was found
    if "results" not in city_data:
        return None


    # Get the first result
    city_information = city_data["results"][0]


    # Get latitude and longitude
    latitude = city_information["latitude"]
    longitude = city_information["longitude"]


    # Return the coordinates
    return latitude, longitude


def get_weather(city):

    # First, find the coordinates of the city
    coordinates = get_city_coordinates(city)


    # Check if the city was found
    if coordinates is None:
        return None


    # Get latitude and longitude
    latitude = coordinates[0]
    longitude = coordinates[1]


    # Open-Meteo Weather API
    weather_url = "https://api.open-meteo.com/v1/forecast"


    # Information we want from the Weather API
    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto"
    }


    # Send request to the Weather API
    response = requests.get(weather_url, params=parameters)


    # Convert JSON response into a Python dictionary
    weather_data = response.json()


    # Get current weather
    current_weather = weather_data["current"]


    # Get individual weather values
    temperature = current_weather["temperature_2m"]
    humidity = current_weather["relative_humidity_2m"]
    wind_speed = current_weather["wind_speed_10m"]
    weather_code = current_weather["weather_code"]
    # Get today's forecast information
    daily_weather = weather_data["daily"]
    # Get today's maximum temperature
    maximum_temperature = daily_weather["temperature_2m_max"][0]
    # Get today's minimum temperature
    minimum_temperature = daily_weather["temperature_2m_min"][0]


    # Get today's chance of rain
    rain_probability = daily_weather["precipitation_probability_max"][0]

    #encoding weather code
    if weather_code == 0:
        weather_condition = "Clear sky"

    elif weather_code in [1, 2, 3]:
        weather_condition = "Cloudy"

    elif weather_code in [45, 48]:
        weather_condition = "Fog"

    elif weather_code in [51, 53, 55, 56, 57]:
        weather_condition = "Drizzle"

    elif weather_code in [61, 63, 65, 66, 67]:
        weather_condition = "Rain"

    elif weather_code in [71, 73, 75, 77]:
        weather_condition = "Snow"

    elif weather_code in [80, 81, 82]:
        weather_condition = "Rain showers"

    elif weather_code in [95, 96, 99]:
        weather_condition = "Thunderstorm"

    else:
        weather_condition = "Unknown"


    # Create our own simple weather dictionary
    weather_information = {
        "city": city,

        "temperature": temperature,

        "humidity": humidity,

        "wind_speed": wind_speed,

        "weather_condition": weather_condition,

        "maximum_temperature": maximum_temperature,

        "minimum_temperature": minimum_temperature,

        "rain_probability": rain_probability
    }


    return weather_information

