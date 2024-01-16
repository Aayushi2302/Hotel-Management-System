from marshmallow import Schema, fields, validate
from config.regex_pattern import RegexPattern

class EmployeeSchema(Schema):
    employee_id = fields.Str(dump_only=True)
    username = fields.Str(required=True, validate=validate.Regexp(RegexPattern.USERNAME_REGEX))
    password = fields.Str(dump_only=True)
    role = fields.Str(required=True, validate=validate.Regexp(RegexPattern.ROLE_REGEX))
    password_type = fields.Str(dump_only=True)
