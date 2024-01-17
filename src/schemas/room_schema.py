from marshmallow import Schema, fields, validate
from config.regex_pattern import RegexPattern

class RoomSchema(Schema):
    room_id = fields.Str(dump_only=True)
    room_no = fields.Int(required=True)
    floor_no = fields.Int(required=True)
    charges = fields.Float(required=True)
    status = fields.Str(dump_only=True)

class RoomSchemaUpdate(Schema):
    room_no = fields.Int(required=True)
    floor_no = fields.Int(required=True)
    status = fields.Str(required=True, validate=validate.Regexp(RegexPattern.ROOM_STATUS))

    