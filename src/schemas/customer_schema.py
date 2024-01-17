from marshmallow import Schema, fields, validate
from config.regex_pattern import RegexPattern

class CustomerSchema(Schema):
    cust_id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Regexp(RegexPattern.NAME_REGEX))
    age = fields.Str(required=True, validate=validate.Regexp(RegexPattern.AGE_REGEX))
    gender = fields.Str(required=True)
    email = fields.Str(required=True, validate=validate.Regexp(RegexPattern.EMAIL_REGEX))
    mobile_number = fields.Str(required=True, validate=validate.Regexp(RegexPattern.MOBILE_NO_REGEX))
    status = fields.Str(dump_only=True)

class CustomerUpdateSchema(Schema):
    cust_email = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)

class DemoSchema(Schema):
    price = fields.Float(required=True)