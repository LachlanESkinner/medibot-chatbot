#Import required libraries
import os
import requests
import asyncio
import aiohttp
import json
import logging
import nest_asyncio
from flask import Flask, request, render_template, jsonify
from cachetools import TTLCache
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from locations import get_coordinates, get_all_locations
import time
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

#SQLAlchemy setup
Base = declarative_base()
engine = create_engine("sqlite:///forecast.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class Forecast(Base):
    __tablename__ = "forecasts"
    id = Column(Integer, primary_key=True)
    location = Column(String)
    date = Column(DateTime)
    temp = Column(Float)
    description = Column(String)

Base.metadata.create_all(bind=engine)

#Async event loop support
nest_asyncio.apply()

#Loging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#flask app
app = Flask(__name__)

#ChatterBot setup
chatbot = ChatBot(
    "PyBot",
    read_only=True,
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.BestMatch"
    ]
)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

#Read API key
def get_api_key():
    try:
        with open("api_key.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception("API key file not found.")

API_KEY = get_api_key()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

#Caching & performance
cache = TTLCache(maxsize=50, ttl=600)
performance_metrics = {
    'total_requests': 0,
    'cached_responses': 0,
    'api_latency': []
}

#Fetch current weather
async def fetch_weather(location, lat, lon):
    if location in cache:
        performance_metrics['cached_responses'] += 1
        return cache[location]

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        async with session.get(BASE_URL, params=params) as response:
            performance_metrics['total_requests'] += 1
            if response.status == 200:
                data = await response.json()
                cache[location] = data
                performance_metrics['api_latency'].append(time.time() - start_time)
                return data
            elif response.status == 401:
                return {"error": "Unauthorized access. Please verify your API key."}
            else:
                return {"error": f"API request failed for {location}"}

#Fetch 5-day forecast and store in DB
def fetch_and_store_forecast(location):
    lat, lon = get_coordinates(location)
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        forecast_list = response.json().get("list", [])
        session.query(Forecast).filter_by(location=location).delete()
        for item in forecast_list:
            entry = Forecast(
                location=location,
                date=datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S"),
                temp=item["main"]["temp"],
                description=item["weather"][0]["description"]
            )
            session.add(entry)
        session.commit()
        return True
    else:
        return False

#retrieve 5-day forecast from DB
def get_forecast_from_db(location):
    forecasts = session.query(Forecast).filter_by(location=location).order_by(Forecast.date).limit(5).all()
    return forecasts

#Flask Routes
@app.route("/")
def home():
    return render_template("index.html", locations=get_all_locations())

@app.route("/weather", methods=["GET", "POST"])
def get_weather():
    if request.method == "POST":
        location = request.form.get("location")
        coordinates = get_coordinates(location)
        if not coordinates:
            return render_template("results.html", error="Invalid location selected.")
        lat, lon = coordinates
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        weather_data = loop.run_until_complete(fetch_weather(location, lat, lon))
        loop.close()
        return render_template("results.html", weather=weather_data, location=location, lat=lat, lon=lon)
    return render_template("form.html", locations=get_all_locations())

@app.route("/metrics")
def metrics():
    avg_latency = sum(performance_metrics['api_latency']) / len(performance_metrics['api_latency']) if \
    performance_metrics['api_latency'] else 0
    return render_template("metrics.html", metrics=performance_metrics, avg_latency=avg_latency)

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/chatbot", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()
    matched_locations = [loc for loc in get_all_locations() if loc.lower() in user_message]

    if "forecast" in user_message and matched_locations:
        location = matched_locations[0]
        fetch_and_store_forecast(location)
        forecasts = get_forecast_from_db(location)
        if not forecasts:
            return jsonify({"response": f"No forecast data found for {location}."})
        response = f"🌦️ 5-Day Forecast for {location.title()}:\n"
        for f in forecasts:
            response += f"{f.date.strftime('%a %b %d')}: {f.temp}°C, {f.description.capitalize()}\n"
        response += f"\nWould you like suggestions for activities in {location.title()}?"
        return jsonify({"response": response})

    elif matched_locations:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        responses = []
        follow_ups = []
        for loc in matched_locations:
            lat, lon = get_coordinates(loc)
            weather = loop.run_until_complete(fetch_weather(loc, lat, lon))
            if "error" in weather:
                responses.append(f"{loc.title()}: {weather['error']}")
            else:
                temp = weather['main']['temp']
                desc = weather['weather'][0]['description']
                summary = f"Currently in {loc.title()}, it’s {temp}°C with {desc}."

                if "clear" in desc or "sun" in desc:
                    activity = f"It’s a great time for outdoor activities like hiking, cycling, or visiting landmarks in {loc.title()}."
                elif "rain" in desc or "storm" in desc:
                    activity = f"Consider indoor attractions like museums or cafes while it's rainy in {loc.title()}."
                elif "cloud" in desc:
                    activity = f"A cloudy day in {loc.title()} — perfect for a scenic walk or relaxed exploring."
                else:
                    activity = f"Weather might be mixed — keep a raincoat handy and enjoy what {loc.title()} has to offer!"

                responses.append(summary)
                follow_ups.append(activity)

        loop.close()
        return jsonify({"response": "\n".join(responses + follow_ups) + "\n\nWould you like a 5-day forecast too?"})

    else:
        bot_response = chatbot.get_response(user_message)
        return jsonify({"response": str(bot_response)})

#Run the app
if __name__ == "__main__":
    app.run(debug=True)
