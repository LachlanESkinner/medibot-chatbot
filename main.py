# Main.py — Mediplast AI Chatbot
# Ensure correct environment: source chatbot_env37/bin/activate

# Insert patched ChatterBot path first
import sys
sys.path.insert(0, 'patched_chatterbot')

# Import libraries
import os
import asyncio
import logging
import nest_asyncio
from flask import Flask, request, render_template, jsonify
from cachetools import TTLCache
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from chatbot_training_data import training_data

# Async event loop support
nest_asyncio.apply()

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask app
app = Flask(__name__)

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine("sqlite:///chat_logs.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True)
    user_message = Column(String)
    bot_response = Column(String)
    intent = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ChatterBot setup (corpus-free)
chatbot = ChatBot(
    "MediBot",
    read_only=True,
    logic_adapters=[
        "chatterbot.logic.BestMatch"
    ]
)

# Train the chatbot (using only your custom data)
trainer = ListTrainer(chatbot)
trainer.train(training_data)

# Cache setup
cache = TTLCache(maxsize=50, ttl=600)

# --- Intent Classification ---
def infer_intent(message):
    msg = message.lower()
    if "ndis" in msg:
        return "Funding - NDIS"
    elif "caps" in msg:
        return "Funding - CAPS"
    elif "dva" in msg:
        return "Funding - DVA"
    elif "navina" in msg:
        return "Product - Navina"
    elif "lofric" in msg:
        return "Product - LoFric"
    elif "sample" in msg:
        return "General - Sample"
    elif "order" in msg or "shipping" in msg:
        return "Support - Order"
    else:
        return "General"

# Routes

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form.get("message", "").lower()
        bot_response = chatbot.get_response(user_message)
        intent = infer_intent(user_message)

        chat_log = ChatLog(user_message=user_message, bot_response=str(bot_response), intent=intent)
        session.add(chat_log)
        session.commit()

        return render_template("chat.html", user_message=user_message, bot_response=str(bot_response))

    return render_template("chat.html")

@app.route("/chatbot", methods=["POST"])
def api_chat():
    user_message = request.json.get("message", "").lower()
    bot_response = chatbot.get_response(user_message)
    intent = infer_intent(user_message)

    chat_log = ChatLog(user_message=user_message, bot_response=str(bot_response), intent=intent)
    session.add(chat_log)
    session.commit()

    return jsonify({"response": str(bot_response), "intent": intent})

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
