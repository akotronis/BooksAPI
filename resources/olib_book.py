import time

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from populate import FeedDB
from schemas import QueryOlibBookSchema


blp_v1 = Blueprint("Openlib-books-v1", __name__)

# @jwt_required
@blp_v1.route('/olib-books')
class OlibBook(MethodView):

    # @jwt_required()
    @blp_v1.arguments(QueryOlibBookSchema, location='query')
    @blp_v1.response(201)
    def get(self, query_args):
        try:
            asynchronously = query_args.get('asynchronously')
            feed = FeedDB(asynchronously)
            start = time.time()
            feed.fetch_all_books_data()
            books_count = feed.populate_database()
            perf_time = time.time() - start
        except:
            abort(500, message='Could not fetch books from open library')
        return {"code": 201, "status":"Created", 'message': f'Fetched {books_count} books from open library in {perf_time:.2f} sec. Database objects created.'}
