from marshmallow import Schema, fields


class BookAndAuthorSchema(Schema):
    book = fields.Nested('BookSchema')
    author = fields.Nested('AuthorSchema')