from marshmallow import fields
from schemas import PlainBookSchema


class BookAndWorkSchema(PlainBookSchema):
    works = fields.List(fields.Nested('PlainWorkSchema'), dump_only=True)