# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_restx import Api
# from .database import db
# from .routes import api as todo_namespace
# from .auth import api as auth_namespace
# from dotenv import load_dotenv
# import os

# load_dotenv()  # Load environment variables from .env

# def create_app():
#     app = Flask(__name__)

#     # Config
#     app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

#     # Initialize extensions
#     db.init_app(app)

#     # API & Namespaces
#     api = Api(app, version="1.0", title="ToDo API", doc="/docs")
#     api.add_namespace(todo_namespace, path="/todos")
#     api.add_namespace(auth_namespace, path="/auth")

#     return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from .database import db
from .auth import api as auth_api
from .routes import api as todos_api
from .protected import api as protected_api  # 👈 new
from .jwt import jwt
from dotenv import load_dotenv
import os

load_dotenv()

# 🔐 Swagger auth config
authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Add 'Bearer <JWT>'"
    }
}

# 👇 API instance (without app)
api = Api(
    version="1.0",
    title="ToDo API",
    doc="/docs"
)
# Set security config
api.authorizations = authorizations
# api.security = "Bearer Auth"

def create_app():
    app = Flask(__name__)

    # Config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)  # 👈 connect Flask app to API

    # Register namespaces
    api.add_namespace(todos_api, path="/todos")
    api.add_namespace(auth_api, path="/auth")
    api.add_namespace(protected_api, path="/protected")  # 👈 protected route

    return app
