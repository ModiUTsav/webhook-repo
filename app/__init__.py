# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # You can add configuration here if needed
    # app.config.from_object('config.Config') # Example if you have a config file

    # Initialize extensions (like MongoDB)
    from .extension import mongo
    mongo.init_app(app) # Assuming you set up init_app in extensions.py

    # Register blueprints or routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app