
Lachlans Weather App with Flask and Leaflet.js

The aim of this file is to provide clarity around the applications use.  

This project is a web-based weather application built using Flask, Leaflet.js, and the OpenWeatherMap API. It allows users to:
- Retrieve current weather data for predefined locations.
- Visualise weather locations on an interactive map.
- Chat with a bot that provides weather info, follow-up suggestions, and activity recommendations.
- View a 5-day forecast stored in a SQL database.
- Track API performance metrics like response time and caching.

How to Use

Start the Flask App:

activate correct environment:

source chatbot_env/bin/activate

python main.py

Access the App in Your Browser:

http://127.0.0.1:5000/

API Endpoints

1. GET / - Home Page  
Displays the homepage with links to weather, chatbot, and metrics tools.

2. GET /weather - Weather Form  
Form for selecting a location to check the weather.

Example Request:  
GET /weather

3. POST /weather - Retrieve Current Weather Data  
Submits a location and fetches current weather data.

Body Parameter:
- location (string): Name of the location (e.g., "Bristol")

Example Request:
POST /weather  
Content-Type: application/x-www-form-urlencoded  
location=Cambridge  

Example Response:
{
  "main": {
    "temp": 15.2,
    "humidity": 78
  },
  "weather": [
    {
      "description": "light rain"
    }
  ],
  "wind": {
    "speed": 3.5
  }
}

Status Codes:
- 200 OK – Weather data returned successfully.
- 401 Unauthorized – Invalid or missing API key.
- 500 Internal Server Error – Data fetch failed from API.

4. GET /metrics - Performance Metrics  
Displays data such as:
- Total API requests
- Cached responses
- Average API latency

Example Response:
{
  "total_requests": 10,
  "cached_responses": 4,
  "api_latency": [0.23, 0.19, 0.21],
  "average_latency": 0.21
}

5. POST /chatbot - Weather Chatbot  
This endpoint allows for chatting with the bot.  
Users can ask:
- “What’s the weather in Oxford?”
- “Give me a 5 day forecast for Norwich”
- “What should I do in Corfe Castle if it’s raining?”

Bot responds with temperature, conditions, activity tips (if available), or fallback general responses.

Map Integration with Leaflet.js

The app uses Leaflet.js to show the weather location on an interactive map. Markers display:
- Location name  
- Temperature  
- Current weather condition  

Technologies Used

- Flask – Python web framework  
- Leaflet.js – Maps & markers  
- Bootstrap 4 – User-friendly UI  
- OpenWeatherMap API – Weather data provider  
- SQLite & SQLAlchemy – For storing 5-day forecasts  
- ChatterBot – For chatbot logic and fallback conversations  

Note: To use the application, an api_key.txt file is required in the root directory containing a valid OpenWeather API key.
