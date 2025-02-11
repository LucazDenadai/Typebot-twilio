# Typebot with Twilio

This project integrates Typebot with Twilio to create a chatbot that can be accessed via WhatsApp.

## Overview

This project uses Flask to create an API that communicates with Typebot and Twilio. Ngrok is used to expose the API locally for testing.

## Requirements

- Python 3.8+
- Flask
- requests
- pyngrok
- xmltodict

## Installation

python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

pip install -r requirements.txt

Create a .env file in the root of the project and add your Twilio credentials:
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=your_whatsapp_number

Start the Flask server and ngrok:
python run.py