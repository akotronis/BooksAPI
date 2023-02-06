from db import db

class WorkModel(db.Model):
    __tablename__ = "works"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=False, nullable=False)
    books = db.relationship("BookModel", back_populates="works", secondary="books_works")

    def __repr__(self):
        return f'<Work "{self.code}">'