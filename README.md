# MediBot — Mediplast AI Chatbot

MediBot is a Flask-based AI chatbot tailored for Mediplast's customer needs. It assists users with questions about products (LoFric, Navina, etc.), funding pathways (NDIS, CAPS, DVA), orders, and general support.

## Features

- AI-powered chatbot using ChatterBot
- SQLite database for logging messages with SQLAlchemy
- Intent inference for basic classification
- Lightweight Flask interface (HTML/CSS provided)
- Read-only mode for safe deployment
- Caching with cachetools for performance
- Easily extensible for future APIs or integrations

## Folder Structure

.
├── main.py
├── chatbot_training_data.py
├── templates/
│   ├── index.html
│   └── chat.html
├── static/
│   ├── styles.css
│   └── images/
├── chat_logs.db
├── requirements.txt
└── README.md

## Setup Instructions

1. Clone the repository

   git clone https://github.com/your-org/medibot-chatbot.git
   cd medibot-chatbot

2. Create and activate a virtual environment

   python3 -m venv chatbot_env
   source chatbot_env/bin/activate

3. Install dependencies

   pip install -r requirements.txt

4. Run the application

   python main.py

   Access the chatbot in your browser at: http://localhost:5000

## Requirements

See requirements.txt for exact package versions used.

## Logging

Conversations are logged to a local SQLite database (chat_logs.db) including:

- user message
- bot response
- inferred intent
- timestamp

## Customization

- To update training data: modify chatbot_training_data.py
- To change HTML: edit templates/index.html or chat.html
- To change styling: edit static/styles.css

## License

MIT License © 2025 Mediplast AI Team
