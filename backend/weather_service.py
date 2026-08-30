import requests


# ---------------------------------------
# Find city coordinates
# ---------------------------------------

def get_city_coordinates(city):

    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    parameters = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:

        response = requests.get(
            geocoding_url,
            params=parameters,
            timeout=10
        )

        response.raise_for_status()

        city_data = response.json()

    except requests.exceptions.RequestException:
        return None

    if "results" not in city_data:
        return None

    city_information = city_data["results"][0]

    latitude = city_information["latitude"]
    longitude = city_information["longitude"]

    return latitude, longitude


# ---------------------------------------
# Get weather data from Open-Meteo
# ---------------------------------------

def get_weather_data(city):

    coordinates = get_city_coordinates(city)

    if coordinates is None:
        return None

    latitude = coordinates[0]
    longitude = coordinates[1]

    weather_url = "https://api.open-meteo.com/v1/forecast"

    parameters = {
        "latitude": latitude,
        "longitude": longitude,

        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",

        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code,wind_speed_10m_max",

        "timezone": "auto",

        "forecast_days": 7
    }

    try:

        response = requests.get(
            weather_url,
            params=parameters,
            timeout=10
        )

        response.raise_for_status()

        weather_data = response.json()

    except requests.exceptions.RequestException:
        return None

    return weather_data


# ---------------------------------------
# Convert weather code
# ---------------------------------------

def get_weather_condition(weather_code):

    if weather_code == 0:
        return "Clear sky"

    elif weather_code in [1, 2, 3]:
        return "Cloudy"

    elif weather_code in [45, 48]:
        return "Fog"

    elif weather_code in [51, 53, 55, 56, 57]:
        return "Drizzle"

    elif weather_code in [61, 63, 65, 66, 67]:
        return "Rain"

    elif weather_code in [71, 73, 75, 77]:
        return "Snow"

    elif weather_code in [80, 81, 82]:
        return "Rain showers"

    elif weather_code in [95, 96, 99]:
        return "Thunderstorm"

    else:
        return "Unknown"


# ---------------------------------------
# Current weather
# ---------------------------------------

def get_weather(city):

    weather_data = get_weather_data(city)

    if weather_data is None:
        return None

    current_weather = weather_data["current"]

    daily_weather = weather_data["daily"]

    weather_code = current_weather["weather_code"]

    weather_information = {

        "city": city,

        "temperature": current_weather["temperature_2m"],

        "humidity": current_weather["relative_humidity_2m"],

        "wind_speed": current_weather["wind_speed_10m"],

        "weather_condition": get_weather_condition(weather_code),

        "maximum_temperature": daily_weather["temperature_2m_max"][0],

        "minimum_temperature": daily_weather["temperature_2m_min"][0],

        "rain_probability": daily_weather["precipitation_probability_max"][0]
    }

    return weather_information


# ---------------------------------------
# 7-Day forecast
# ---------------------------------------

def get_forecast(city):

    weather_data = get_weather_data(city)

    if weather_data is None:
        return None

    daily_weather = weather_data["daily"]

    dates = daily_weather["time"]

    maximum_temperatures = daily_weather["temperature_2m_max"]

    minimum_temperatures = daily_weather["temperature_2m_min"]

    rain_probabilities = daily_weather["precipitation_probability_max"]

    weather_codes = daily_weather["weather_code"]

    forecast = []

    for i in range(len(dates)):

        day_information = {

            "date": dates[i],

            "maximum_temperature": maximum_temperatures[i],

            "minimum_temperature": minimum_temperatures[i],

            "rain_probability": rain_probabilities[i],

            "weather_condition":
                get_weather_condition(weather_codes[i])
        }

        forecast.append(day_information)

    return {

        "city": city,

        "forecast": forecast
    }


# ---------------------------------------
# Weather alerts
# ---------------------------------------

def get_alerts(city):

    weather_data = get_weather_data(city)

    if weather_data is None:
        return None

    daily_weather = weather_data["daily"]

    dates = daily_weather["time"]

    weather_codes = daily_weather["weather_code"]

    rain_probabilities = \
        daily_weather["precipitation_probability_max"]

    wind_speeds = \
        daily_weather["wind_speed_10m_max"]

    alerts = []

    for i in range(len(dates)):

        weather_code = weather_codes[i]

        rain_probability = rain_probabilities[i]

        wind_speed = wind_speeds[i]

        # Thunderstorm
        if weather_code in [95, 96, 99]:

            alerts.append({

                "date": dates[i],

                "type": "Thunderstorm",

                "severity": "High",

                "message":
                    "Thunderstorm conditions may occur."
            })

        # Heavy rain
        elif weather_code in [65, 67, 82] or \
                rain_probability >= 80:

            alerts.append({

                "date": dates[i],

                "type": "Heavy Rain",

                "severity": "Medium",

                "message":
                    "High probability of heavy rain."
            })

        # Strong wind
        elif wind_speed >= 50:

            alerts.append({

                "date": dates[i],

                "type": "Strong Wind",

                "severity": "Medium",

                "message":
                    "Strong winds may occur."
            })

    return {

        "city": city,

        "alerts": alerts
    }