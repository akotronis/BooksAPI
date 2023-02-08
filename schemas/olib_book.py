from marshmallow import Schema, fields


class QueryOlibBookSchema(Schema):
    asynchronously = fields.Boolean(load_only=True, required=False, data_key='async')


