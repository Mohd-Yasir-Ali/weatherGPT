"""
WeatherGPT - Member 3 AI/LLM Integration

Receives verified weather data from the backend
and converts it into simple conversational answers.
"""

import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from google import genai


# Load .env
load_dotenv()


# Get Gemini settings
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


# Make sure API key exists
if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Please add your Gemini API key to .env"
    )


# Create Gemini client
client = genai.Client(api_key=API_KEY)


# Rules for WeatherGPT
SYSTEM_INSTRUCTIONS = """
You are WeatherGPT, a friendly conversational weather assistant.

The application backend gives you verified weather data.

IMPORTANT RULES:

1. Use ONLY the weather data provided to you.
2. Never invent weather values.
3. Never guess missing weather information.
4. If the user asks for something that is not in the weather data,
   clearly say that the information is not available.
5. Answer the user's actual question.
6. Use Celsius for temperature.
7. Keep answers simple and easy to understand.
8. Give practical advice when it follows from the supplied data.
9. Do not claim that you personally checked a weather service.
10. Do not use outside weather information.

Return only the answer that should be shown to the user.
"""


def generate_weather_answer(
    weather_data: Dict[str, Any],
    user_question: str
) -> str:

    """
    Takes weather JSON + user's question
    and returns a conversational WeatherGPT answer.
    """

    # Validate weather data
    if not isinstance(weather_data, dict):
        raise ValueError("weather_data must be a dictionary.")

    # Validate question
    if not user_question or not user_question.strip():
        raise ValueError("user_question cannot be empty.")

    # Convert weather data to JSON
    weather_json = json.dumps(
        weather_data,
        ensure_ascii=False,
        indent=2
    )

    # Create the prompt
    prompt = f"""
WEATHER DATA FROM BACKEND:

{weather_json}


USER QUESTION:

{user_question.strip()}
"""

    # Call Gemini Interactions API
    interaction = client.interactions.create(
        model=MODEL,
        input=prompt,
        system_instruction=SYSTEM_INSTRUCTIONS
    )

    # Get the generated answer
    answer = interaction.output_text.strip()

    # Fallback
    if not answer:
        return "Sorry, I couldn't generate a weather answer right now."

    return answer


# Direct test
if __name__ == "__main__":

    sample_weather = {
        "city": "Lucknow",
        "temperature_c": 31,
        "humidity_percent": 72,
        "condition": "Cloudy",
        "rain_probability_percent": 60,
        "wind_speed_kmh": 15
    }

    question = "Will I need an umbrella today?"

    answer = generate_weather_answer(
        sample_weather,
        question
    )

    print("WEATHERGPT:")
    print(answer)