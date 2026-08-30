from fastapi import FastAPI
from weather_service import get_weather, get_forecast,get_alerts


# Create the FastAPI application
app = FastAPI()


# Home page
@app.get("/")
def home():

    return {
        "message": "Welcome to WeatherGPT"
    }


# Weather endpoint
@app.get("/weather")
def weather(city: str):

    # Get weather information for the requested city
    weather_information = get_weather(city)


    # Check if the city was found
    if weather_information is None:

        return {
            "error": "City not found"
        }


    # Return the weather information
    return weather_information

#forecast endpoint
@app.get("/forecast")
def forecast(city: str):

    forecast_data = get_forecast(city)

    if forecast_data is None:
        return {
            "error": "City not found"
        }

    return forecast_data

#alerts endpoint
@app.get("/alerts")
def alerts(city: str):

    alert_data = get_alerts(city)

    if alert_data is None:
        return {
            "error": "City not found"
        }

    return alert_data