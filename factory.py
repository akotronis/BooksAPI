import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from config.config import config_by_name
from blocklist import BLOCKLIST
from db import db

# Necessary for creating tables
import models
from versioning import register_blueprints
# from resources.book import blp as BookBlueprint
# from resources.author import blp as AuthorBlueprint
# from resources.work import blp as WorkBlueprint
# from resources.olib_book import blp as OlibBlueprint
# from resources.user import blp as UserBlueprint


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    # Load environment variables from .env (.flaskenv)
    load_dotenv()
    
    # Initialize Flask-SQLAlchemy and pass app object to connect with
    db.init_app(app)

    # Connect flask_smorest to the app
    api = Api(app)

    # Connect jwt to the app
    jwt = JWTManager(app)

    ################### JWT CONFIGURATION ###################

    # There may be shared computers in which case we might want to keep tokens ('jti' key from JWT claims) after logging out
    # in a BLOCKLIST so that they can't be used for re-logging in from a potentially different person
    # Check if token is in BLOCKLIST. If returns true, error message is sent. Runs when token is CREATED
    # Use it with persistent storage
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # Defines the message the use gets back when token is in blocklist
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description":"The token has been revoked.", "error": "token revoked."}),
            401
        )

    # Defines the message the use gets back when token is in blocklist because needs a fresh one
    @jwt.needs_fresh_token_loader
    def token_non_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description":"The token is not fresh.", "error": "fresh token required."}),
            401
        )

    # Add custom claims. Runs when token is CREATED
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Example: (Look in database to see if user is an admin instead)
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message":"The token has expired.", "error": "token expired."}),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message":"Signature verification failed.", "error": "Invalid token."}),
            401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"description":"Request does not contain an access token.", "error": "Authorization required."}),
            401
        )

    # Not needed with Flask-Migrate
    with app.app_context():
        # Create tables IF NOT EXIST
        db.create_all() 

    # Register Blueprints
    register_blueprints(api)
    return app