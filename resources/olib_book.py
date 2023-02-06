from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from flask import request
from populate import FeedDB


blp = Blueprint("Openlib_book_routes", __name__, url_prefix='/olib-books')


@blp.route('/', methods=['GET'])
def fetch_books():
    try:
        feed = FeedDB()
        result = feed.populate()
    except:
        abort(500, message='Could not fetch books from open library')
    return result
