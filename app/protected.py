# app/protected.py

from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

api = Namespace('protected', description='Protected routes')

@api.route('/secret')
class SecretResource(Resource):
    @api.doc(security='Bearer Auth')  # 🔐 Show lock icon in Swagger
    @jwt_required()
    def get(self):
        return {"msg": "This is a protected route"}
