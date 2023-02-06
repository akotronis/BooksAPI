from marshmallow import fields
from schemas import PlainBookSchema


class BookAndAuthorSchema(PlainBookSchema):
    authors = fields.List(fields.Nested('PlainAuthorSchema'), dump_only=True)