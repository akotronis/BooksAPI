import asyncio
import requests
import time

from book_codes import ALL_BOOK_CODES
from db import db
from models import BookModel, AuthorModel, WorkModel, BooksAuthors, BooksWorks

class FeedDB:
    def __init__(self, asyncronously=True):
        self.asyncronously = asyncronously
        self.book_url_template = 'https://openlibrary.org/books/{}.json'
        self.book_data = {}

    @staticmethod
    def fetch_values_from_list_of_dicts(input_list, key='key'):
        return [item.get(key).split('/')[-1] for item in input_list if item.get(key)]

    def fetch_book_data_sync(self, book_code: str) -> None:
        book_url = self.book_url_template.format(book_code)
        book_dict_data = requests.get(book_url.format(book_code)).json()
        self.book_data[book_code] = book_dict_data

    async def fetch_book_data_async(self, book_code: str) -> None:
        ## python 3.9+
        # await asyncio.to_thread(self.fetch_book_data_sync, book_code)

        ## python < 3.9
        await asyncio.get_running_loop().run_in_executor(None, self.fetch_book_data_sync, book_code)

    @staticmethod
    def clean_tables():
        BooksAuthors.query.delete()
        BooksWorks.query.delete()
        BookModel.query.delete()
        AuthorModel.query.delete()
        WorkModel.query.delete()

    async def _fetch_all_books_data(self):
        self.book_data = {}
        if self.asyncronously:
            await asyncio.gather(*[self.fetch_book_data_async(book_code) for book_code in ALL_BOOK_CODES])
        else:
            for book_code in ALL_BOOK_CODES:
                self.fetch_book_data_sync(book_code)

    def fetch_all_books_data(self):
        asyncio.run(self._fetch_all_books_data())

    def populate_database(self):
        FeedDB.clean_tables()
        for i, (book_code, book_data) in enumerate(self.book_data.items(), 1):
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
        return i


if __name__ == '__main__':
    start = time.time()
    asyncronously = True
    feed = FeedDB(asyncronously)
    results = asyncio.run(feed.fetch_all_books_data())
    print(time.time() - start)
    print(len(feed.book_data))
    print(feed.book_data)