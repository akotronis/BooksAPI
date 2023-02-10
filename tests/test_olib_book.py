import pytest

from book_codes import ALL_BOOK_CODES
from populate import FeedDB

from models import BookModel


@pytest.mark.olib_book
@pytest.mark.usefixtures('app_ctx')
def test_fetch_olib_books(app):
    feed = FeedDB()
    feed.clean_tables()
    client = app.test_client()
    response = client.get("/olib-books?async=True")
    data = response.get_json()
    assert response.status_code == 201
    assert data.get('status') == 'Created'
    assert data.get('message').startswith(f'Fetched {len(ALL_BOOK_CODES)} books from open library in')
    assert all(BookModel.query.filter(BookModel.code == book_code).first() for book_code in ALL_BOOK_CODES)
