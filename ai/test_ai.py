"""
Simple local tests for Member 3's AI integration.

Run:
    python test_ai.py
"""

from ai_service import generate_weather_answer


WEATHER = {
    "city": "Lucknow",
    "temperature_c": 31,
    "humidity_percent": 72,
    "condition": "Cloudy",
    "rain_probability_percent": 60,
    "wind_speed_kmh": 15,
}


def run_test(question: str):
    print("\nUSER:", question)
    print("WEATHERGPT:", generate_weather_answer(WEATHER, question))


if __name__ == "__main__":
    run_test("What's the weather like?")
    run_test("Will I need an umbrella?")
    run_test("How humid is it?")
    run_test("What is the UV index?")  # UV is intentionally missing.
