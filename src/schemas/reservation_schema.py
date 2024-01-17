from marshmallow import Schema, fields, validate
from config.regex_pattern import RegexPattern

class ReservationCheckInSchema(Schema):
    reservation_id = fields.Str(dump_only=True)
    cust_email = fields.Str(required=True)
    cust_checkin_date = fields.Str(dump_only=True)
    cust_checkin_time = fields.Str(dump_only=True)
    cust_checkout_date = fields.Str(required=True)
    cust_checkout_time = fields.Str(required=True)

class ReservationCheckOutSchema(Schema):
    cust_email = fields.Str(required=True)
    cust_checkout_date = fields.Str(dump_only=True)
    cust_checkout_time = fields.Str(dump_only=True)
    charges = fields.Str(dump_only=True)

