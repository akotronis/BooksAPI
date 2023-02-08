from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import AuthorModel
from schemas import AuthorSchema, UpdateAuthorSchema


blp_v1 = Blueprint("Authors-v1", __name__)


@blp_v1.route("/authors/<int:author_id>")
class Author(MethodView):

    # @jwt_required()
    @blp_v1.response(200, AuthorSchema)
    def get(self, author_id):
        author = AuthorModel.query.get_or_404(author_id)
        return author
    
    # @jwt_required()
    @blp_v1.arguments(UpdateAuthorSchema)
    @blp_v1.response(200, AuthorSchema)
    def put(self, author_data, author_id):
        author = AuthorModel.query.get_or_404(author_id)
        try:
            author_code = author_data.get('code')
            if author_code is not None:
                author.code = author_code
        except:
            db.session.rollback()
            abort(500, message="Could not update author")
        else:
            db.session.commit()
        return author

    #@jwt_required()
    def delete(self, author_id):
        author = AuthorModel.query.get_or_404(author_id)
        try:
            db.session.delete(author)
        except:
            db.session.rollback()
            abort(500, message="Could not delete author")
        else:
            db.session.commit()
        return {"code": 200, "status":"OK"}


@blp_v1.route("/authors")
class AuthorList(MethodView):
    
    # @jwt_required()
    @blp_v1.response(200, AuthorSchema(many=True))
    def get(self):
        return AuthorModel.query.all()

    # @jwt_required()
    @blp_v1.arguments(AuthorSchema)
    @blp_v1.response(201, AuthorSchema)
    def post(self, author_data):
        try:
            author = AuthorModel(**author_data)
            db.session.add(author)
        except:
            db.session.rollback()
            abort(500, message="Could not create author")
        else:
            db.session.commit()
        return author
    



    
