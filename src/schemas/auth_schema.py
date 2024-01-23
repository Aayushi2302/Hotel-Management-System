from marshmallow import Schema, fields

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    

class LoginResponseSchema(Schema):
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)
    message = fields.Str(dump_only=True)