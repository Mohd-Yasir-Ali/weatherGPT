import requests


# Open-Meteo Geocoding API
url = "https://geocoding-api.open-meteo.com/v1/search"


# The city we want to search for
city = "Delhi"


# Information we are sending to the API
parameters = {
    "name": city,
    "count": 1,
    "language": "en",
    "format": "json"
}


# Send a GET request to the Geocoding API
response = requests.get(url, params=parameters)


# Convert the JSON response into a Python dictionary
city_data = response.json()


# Print the complete response
print(city_data)