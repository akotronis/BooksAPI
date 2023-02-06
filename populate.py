import json
import requests

from book_codes import ALL_BOOK_CODES
from db import db
from models import BookModel, AuthorModel, WorkModel, BooksAuthors, BooksWorks

class FeedDB:
    def __init__(self):
        self.book_url_template = 'https://openlibrary.org/books/{}.json'

    @staticmethod
    def fetch_values_from_list_of_dicts(input_list, key='key'):
        return [item.get(key).split('/')[-1] for item in input_list if item.get(key)]

    def fetch_book_data(self, book_code: str) -> dict:
        book_url = self.book_url_template.format(book_code)
        book_text_data = requests.get(book_url.format(book_code)).text
        book_dict = json.loads(book_text_data)
        return book_dict

    @staticmethod
    def clean_tables():
        BooksAuthors.query.delete()
        BooksWorks.query.delete()
        BookModel.query.delete()
        AuthorModel.query.delete()
        WorkModel.query.delete()

    def populate(self):
        FeedDB.clean_tables()
        for i, book_code in enumerate(ALL_BOOK_CODES, 1):
            book_data = self.fetch_book_data(book_code)
            book_title = book_data.get('title')
            
            book = BookModel(code=book_code, title=book_title)
            db.session.add(book)

            book_works = FeedDB.fetch_values_from_list_of_dicts(book_data.get('works', []))
            for work_code in book_works:
                work_obj = WorkModel(code=work_code)
                book.works.append(work_obj)
                db.session.add(work_obj)

            book_authors = FeedDB.fetch_values_from_list_of_dicts(book_data.get('authors', []))
            for author_code in book_authors:
                author_obj = AuthorModel(code=author_code)
                book.authors.append(author_obj)
                db.session.add(author_obj)
        db.session.commit()
        return {'Message': f'Fetched {i} books from open library'}
