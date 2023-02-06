from sqlalchemy import UniqueConstraint
from db import db

class BooksWorks(db.Model):
    __tablename__ = "books_works"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    work_id = db.Column(db.Integer, db.ForeignKey("works.id"))