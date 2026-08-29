import requests


# Open-Meteo API URL
url = "https://api.open-meteo.com/v1/forecast"


# Coordinates for Lucknow
latitude = 26.8467
longitude = 80.9462


# Information we want from the weather API
parameters = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
}


# Send a GET request to the weather API
response = requests.get(url, params=parameters)


# Convert the response from JSON into a Python dictionary
weather_data = response.json()


# Get the "current" weather information
current_weather = weather_data["current"]


# Get individual weather values
temperature = current_weather["temperature_2m"]
humidity = current_weather["relative_humidity_2m"]
wind_speed = current_weather["wind_speed_10m"]


# Display the weather information
print("Temperature:", temperature, "°C")
print("Humidity:", humidity, "%")
print("Wind Speed:", wind_speed, "km/h")
