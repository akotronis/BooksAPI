from db import db

class BookModel(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=False, nullable=False)
    title = db.Column(db.String(200), unique=False, nullable=False)
    authors = db.relationship("AuthorModel", back_populates="books", secondary="books_authors", cascade="all, delete")
    works = db.relationship("WorkModel", back_populates="books", secondary="books_works", cascade="all, delete")

    def __repr__(self):
        return f'<Book "{self.code}">'