from marshmallow import Schema, fields


class PlainAuthorSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True)


class UpdateAuthorSchema(Schema):
    code = fields.Str()


class AuthorSchema(PlainAuthorSchema):
    books = fields.List(fields.Nested('PlainBookSchema'), dump_only=True)