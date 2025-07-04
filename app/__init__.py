# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Initialize extensions (like MongoDB)
    from .extension import mongo
    mongo.init_app(app) 

    # Register blueprints or routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app