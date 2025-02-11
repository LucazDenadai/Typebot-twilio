from flask import Flask
from app.controllers.typebot_controller import typebot_bp

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('config.Config')

    # Register blueprints or routes here if needed
    app.register_blueprint(typebot_bp)

    return app

app = create_app()