from db import db

class AuthorModel(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=False, nullable=False)
    books = db.relationship("BookModel", back_populates="authors", secondary="books_authors")

    def __repr__(self):
        return f'<Author "{self.code}">'