from flask import request
from flask_restx import Namespace, Resource, fields
from datetime import datetime
import jwt
import os
from functools import wraps

from .models import ToDo, User
from .database import db

api = Namespace("todos", description="ToDo operations")

# Swagger model for ToDo
todo_model = api.model("ToDo", {
    "title": fields.String(required=True),
    "description": fields.String(required=False),
    "due_date": fields.String(required=False, example="2025-08-10"),
    "is_completed": fields.Boolean(default=False)
})

# === JWT DECORATOR ===
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return {"message": "Token is missing!"}, 401

        try:
            data = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
            current_user = User.query.get(data["user_id"])
            if not current_user:
                return {"message": "User not found!"}, 401
        except jwt.ExpiredSignatureError:
            return {"message": "Token expired!"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token!"}, 401

        return f(current_user, *args, **kwargs)
    return decorated


# === CREATE & LIST TODOS ===
@api.route("")
class TodoList(Resource):
    @api.doc(security='Bearer Auth')
    @api.expect(todo_model)
    @token_required
    def post(current_user, self):
        data = request.get_json()
        new_todo = ToDo(
            title=data["title"],
            description=data.get("description"),
            due_date=datetime.strptime(data["due_date"], "%Y-%m-%d") if data.get("due_date") else None,
            is_completed=data.get("is_completed", False),
            user_id=current_user.id
        )
        db.session.add(new_todo)
        db.session.commit()
        return {"message": "ToDo created successfully"}, 201

    @api.doc(security='Bearer Auth')
    @token_required
    def get(current_user, self):
        todos = ToDo.query.filter_by(user_id=current_user.id).all()
        result = [{
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "due_date": todo.due_date.strftime("%Y-%m-%d") if todo.due_date else None,
            "is_completed": todo.is_completed
        } for todo in todos]

        return {"todos": result}, 200
