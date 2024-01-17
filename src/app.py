from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from functools import wraps

from src.models.database import db
from src.resources.auth_resource import blp as AuthBlueprint
from src.resources.admin_resource import blp as AdminBlueprint
from src.resources.room_resource import blp as RoomBlueprint
from src.resources.customer_resource import blp as CustomerBlueprint
from src.resources.reservation_resource import blp as ReservationBlueprint
from blocklist import BLOCKLIST

def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Hotel Management System REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    db.create_all_tables()

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "203332112978882378598017085047916523927"
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    api.register_blueprint(AuthBlueprint)
    api.register_blueprint(AdminBlueprint)
    api.register_blueprint(RoomBlueprint)
    api.register_blueprint(CustomerBlueprint)
    api.register_blueprint(ReservationBlueprint)

    return app
