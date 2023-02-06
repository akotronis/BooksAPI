from marshmallow import Schema, fields


class PlainWorkSchema(Schema):
    class Meta:
        ordered = True  
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True)


class UpdateWorkSchema(Schema):
    code = fields.Str()


class WorkSchema(PlainWorkSchema):
    books = fields.List(fields.Nested('PlainBookSchema'), dump_only=True)