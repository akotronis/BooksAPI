from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import BookModel, AuthorModel, WorkModel
from schemas import PlainBookSchema, QueryBookSchema, BookSchema, UpdateBookSchema, BookAndAuthorSchema, BookAndWorkSchema


blp_v1 = Blueprint("Books-v1", __name__)
blp_v2 = Blueprint("Books-v2", __name__)


@blp_v2.route("/books/<int:book_id>")
class Book(MethodView):

    # @jwt_required()
    @blp_v2.response(200, BookSchema)
    def get(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        return book
    
    # @jwt_required()
    @blp_v2.arguments(UpdateBookSchema)
    @blp_v2.response(200, BookSchema)
    def put(self, book_data, book_id):
        book = BookModel.query.get_or_404(book_id)
        try:
            book_code = book_data.get('code')
            if book_code is not None:
                book.code = book_code
            book_title = book_data.get('title')
            if book_title is not None:
                book.title = book_title
        except:
            db.session.rollback()
            abort(500, message="Could not update book")
        else:
            db.session.commit()
        return book

    # @jwt_required()
    def delete(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        try:
            db.session.delete(book)
        except:
            db.session.rollback()
            abort(500, message="Could not delete book")
        else:
            db.session.commit()
        return {"code": 200, "status":"OK"}


@blp_v1.route("/books")
class BookListV1(MethodView):
    
    # @jwt_required()
    @blp_v1.response(200)
    def get(self):
        return {'message':'Book Version 1'}

    # @jwt_required()
    @blp_v1.arguments(PlainBookSchema)
    @blp_v1.response(201, BookSchema)
    def post(self, book_data):
        try:
            book = BookModel(**book_data)
            db.session.add(book)
        except:
            db.session.rollback()
            abort(500, message="Could not create book")
        else:
            db.session.commit()
        return book


@blp_v2.route("/books")
class BookListV2(BookListV1):
    
    @jwt_required()
    @blp_v2.arguments(QueryBookSchema, location='query')
    @blp_v2.response(200, BookSchema(many=True))
    def get(self, query_args):
        contain_substring = query_args.get('contains')
        if contain_substring:
            return BookModel.query.filter(BookModel.title.contains(contain_substring)).all()
        return BookModel.query.all()


@blp_v2.route("/books/<int:book_id>/authors/<int:author_id>")
class LinkBookToAuthor(MethodView):
    '''(Link a book to an author) Add a row to "books_authors" table
    '''

    # @jwt_required()
    @blp_v2.response(201, BookAndAuthorSchema)
    def post(self, book_id, author_id):
        book = BookModel.query.get_or_404(book_id)
        author = AuthorModel.query.get_or_404(author_id)
        if author in book.authors:
            abort(400, message="This book-author pair already exists")
        try:
            book.authors.append(author)
            db.session.add(book)
        except:
            db.session.rollback()
            abort(500, message="Could not create book-author pair")
        else:
            db.session.commit()
        return book


@blp_v2.route("/books/<int:book_id>/works/<int:work_id>")
class LinkBookToWork(MethodView):
    '''(Link a book to a work) Add a row to "books_works" table
    '''
    
    # @jwt_required()
    @blp_v2.response(201, BookAndWorkSchema)
    def post(self, book_id, work_id):
        book = BookModel.query.get_or_404(book_id)
        work = WorkModel.query.get_or_404(work_id)
        if work in book.works:
            abort(400, message="This book-work pair already exists")
        try:
            book.works.append(work)
            db.session.add(book)
        except:
            db.session.rollback()
            abort(500, message="Could not create book-work pair")
        else:
            db.session.commit()
        return book
