from marshmallow import Schema, fields


class BookAndWorkSchema(Schema):
    book = fields.Nested('BookSchema')
    work = fields.Nested('AuthorSchema')