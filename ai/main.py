"""
Optional standalone FastAPI wrapper for Member 3's AI module.

This lets the team test your AI integration independently before
merging it into the main backend.

Run:
    uvicorn main:app --reload

Then open:
    http://127.0.0.1:8000/docs
"""

from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ai_service import generate_weather_answer

app = FastAPI(
    title="WeatherGPT AI Service",
    description="Member 3 - LLM integration for WeatherGPT",
    version="1.0.0",
)


class WeatherChatRequest(BaseModel):
    weather_data: Dict[str, Any] = Field(
        ...,
        description="Verified weather JSON received from the backend."
    )
    question: str = Field(
        ...,
        min_length=1,
        description="The user's weather question."
    )


class WeatherChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {
        "service": "WeatherGPT AI",
        "member": "Member 3",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ai/chat", response_model=WeatherChatResponse)
def ai_chat(request: WeatherChatRequest):
    try:
        answer = generate_weather_answer(
            request.weather_data,
            request.question,
        )
        return WeatherChatResponse(answer=answer)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        # Do not expose API keys or internal provider errors to users.
        raise HTTPException(
            status_code=500,
            detail="AI service could not generate a response."
        )
