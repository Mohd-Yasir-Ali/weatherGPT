async function getWeather() {

    // Get city entered by the user
    const city = document.getElementById("cityInput").value;

    // Check if city is empty
    if (city.trim() === "") {
        showError("Please enter a city name.");
        return;
    }


    // Show loading message
    document.getElementById("loading").classList.remove("hidden");

    // Hide previous results
    document.getElementById("weatherSection").classList.add("hidden");
    document.getElementById("errorSection").classList.add("hidden");


    try {

        // Call our FastAPI backend
        const weatherResponse = await fetch(
            `http://127.0.0.1:8000/weather?city=${encodeURIComponent(city)}`
        );


        // Convert response to JavaScript object
        const weatherData = await weatherResponse.json();


        // Check for error
        if (weatherData.error) {
            showError(weatherData.error);
            return;
        }


        // Display current weather
        document.getElementById("cityName").textContent =
            weatherData.city;

        document.getElementById("temperature").textContent =
            weatherData.temperature;

        document.getElementById("humidity").textContent =
            weatherData.humidity + "%";

        document.getElementById("windSpeed").textContent =
            weatherData.wind_speed + " km/h";

        document.getElementById("rainProbability").textContent =
            weatherData.rain_probability + "%";

        document.getElementById("weatherCondition").textContent =
            weatherData.weather_condition;


        // Get forecast
        await getForecast(city);


        // Get alerts
        await getAlerts(city);


        // Show weather section
        document.getElementById("weatherSection")
            .classList.remove("hidden");

    }

    catch (error) {

        showError(
            "Unable to connect to the weather server."
        );

        console.log(error);

    }

    finally {

        document.getElementById("loading")
            .classList.add("hidden");
    }
}



async function getForecast(city) {

    const response = await fetch(
        `http://127.0.0.1:8000/forecast?city=${encodeURIComponent(city)}`
    );

    const forecastData = await response.json();


    const container =
        document.getElementById("forecastContainer");


    container.innerHTML = "";


    forecastData.forecast.forEach(day => {

        const dayElement =
            document.createElement("div");

        dayElement.className = "forecast-day";


        dayElement.innerHTML = `
            <strong>${day.date}</strong>

            <span>
                ${day.weather_condition}
            </span>

            <span>
                ${day.minimum_temperature}°C -
                ${day.maximum_temperature}°C
            </span>

            <span>
                Rain: ${day.rain_probability}%
            </span>
        `;


        container.appendChild(dayElement);

    });
}



async function getAlerts(city) {

    const response = await fetch(
        `http://127.0.0.1:8000/alerts?city=${encodeURIComponent(city)}`
    );

    const alertData = await response.json();


    const container =
        document.getElementById("alertsContainer");


    container.innerHTML = "";


    if (alertData.alerts.length === 0) {

        container.textContent =
            "No major weather alerts for the forecast period.";

        return;
    }


    alertData.alerts.forEach(alert => {

        const alertElement =
            document.createElement("div");

        alertElement.className = "alert";


        alertElement.innerHTML = `
            <strong>
                ${alert.type} - ${alert.severity}
            </strong>

            <p>
                ${alert.date}: ${alert.message}
            </p>
        `;


        container.appendChild(alertElement);

    });
}



function showError(message) {

    document.getElementById("errorMessage")
        .textContent = message;

    document.getElementById("errorSection")
        .classList.remove("hidden");

    document.getElementById("loading")
        .classList.add("hidden");
}