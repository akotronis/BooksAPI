from marshmallow import Schema, fields


class PlainBookSchema(Schema):
    class Meta:
        ordered = True  
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True)
    title = fields.Str(required=True)


class QueryBookSchema(Schema):
    contains = fields.Str(load_only=True, required=False)


class UpdateBookSchema(Schema):
    code = fields.Str()
    title = fields.Str()


class BookSchema(PlainBookSchema):
    authors = fields.List(fields.Nested('PlainAuthorSchema'), dump_only=True)
    works = fields.List(fields.Nested('PlainWorkSchema'), dump_only=True)




