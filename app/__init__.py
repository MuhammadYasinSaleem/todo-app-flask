from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from .database import db
from .routes import api as todo_namespace
from .auth import api as auth_namespace
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

def create_app():
    app = Flask(__name__)

    # Config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Initialize extensions
    db.init_app(app)

    # API & Namespaces
    api = Api(app, version="1.0", title="ToDo API", doc="/docs")
    api.add_namespace(todo_namespace, path="/todos")
    api.add_namespace(auth_namespace, path="/auth")

    return app
