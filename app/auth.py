from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os

from .models import User
from .database import db

api = Namespace("auth", description="Authentication routes")

# Swagger model for input
signup_model = api.model("SignUp", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

login_model = api.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

# === SIGNUP ===
@api.route("/signup")
class SignUp(Resource):
    @api.expect(signup_model)
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 409

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

# === LOGIN ===
@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401

        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=2)
        }, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")

        return {"token": token}, 200
