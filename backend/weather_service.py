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
def get_forecast(city):

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
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "timezone": "auto",
        "forecast_days": 7
    }

    # Send request to the Weather API
    response = requests.get(weather_url, params=parameters)

    # Convert JSON response into a Python dictionary
    weather_data = response.json()

    # Get daily weather information
    daily_weather = weather_data["daily"]

    # Get the dates
    dates = daily_weather["time"]

    # Get maximum temperatures
    maximum_temperatures = daily_weather["temperature_2m_max"]

    # Get minimum temperatures
    minimum_temperatures = daily_weather["temperature_2m_min"]

    # Get rain probabilities
    rain_probabilities = daily_weather["precipitation_probability_max"]

    # Get weather codes
    weather_codes = daily_weather["weather_code"]

    # Create forecast list
    forecast = []

    # Go through each day
    for i in range(len(dates)):

        weather_code = weather_codes[i]

        # Convert weather code into simple condition
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

        # Create information for this day
        day_information = {
            "date": dates[i],
            "maximum_temperature": maximum_temperatures[i],
            "minimum_temperature": minimum_temperatures[i],
            "rain_probability": rain_probabilities[i],
            "weather_condition": weather_condition
        }

        # Add the day to forecast
        forecast.append(day_information)

    # Create final response
    forecast_information = {
        "city": city,
        "forecast": forecast
    }

    return forecast_information
def get_alerts(city):

    # Get the coordinates of the city
    coordinates = get_city_coordinates(city)

    # Check if city was found
    if coordinates is None:
        return None

    latitude = coordinates[0]
    longitude = coordinates[1]

    # Open-Meteo Weather API
    weather_url = "https://api.open-meteo.com/v1/forecast"

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "weather_code,precipitation_probability_max,wind_speed_10m_max",
        "timezone": "auto",
        "forecast_days": 7
    }

    response = requests.get(weather_url, params=parameters)

    weather_data = response.json()

    daily_weather = weather_data["daily"]

    dates = daily_weather["time"]
    weather_codes = daily_weather["weather_code"]
    rain_probabilities = daily_weather["precipitation_probability_max"]
    wind_speeds = daily_weather["wind_speed_10m_max"]

    alerts = []

    for i in range(len(dates)):

        weather_code = weather_codes[i]
        rain_probability = rain_probabilities[i]
        wind_speed = wind_speeds[i]

        # Thunderstorm alert
        if weather_code in [95, 96, 99]:
            alerts.append({
                "date": dates[i],
                "type": "Thunderstorm",
                "severity": "High",
                "message": "Thunderstorm conditions may occur."
            })

        # Heavy rain alert
        elif weather_code in [65, 67, 82] or rain_probability >= 80:
            alerts.append({
                "date": dates[i],
                "type": "Heavy Rain",
                "severity": "Medium",
                "message": "High probability of heavy rain."
            })

        # Strong wind alert
        elif wind_speed >= 50:
            alerts.append({
                "date": dates[i],
                "type": "Strong Wind",
                "severity": "Medium",
                "message": "Strong winds may occur."
            })

    return {
        "city": city,
        "alerts": alerts
    }

