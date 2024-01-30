from pydantic import BaseModel, Field
from config.regex_pattern import RegexPattern

class ReservationCheckInSchemaArguments(BaseModel):
    cust_email : str = Field(pattern=RegexPattern.EMAIL_REGEX)
    cust_checkout_date : str
    cust_checkout_time : str

class ReservationCheckInSchemaResponse(BaseModel):
    reservation_id : str
    cust_email : str = Field(pattern=RegexPattern.EMAIL_REGEX)
    cust_checkin_date : str
    cust_checkin_time : str
    cust_checkout_date : str
    cust_checkout_time : str

class ReservationCheckOutSchemaArguments(BaseModel):
    cust_email : str = Field(pattern=RegexPattern.EMAIL_REGEX)

class ReservationCheckOutSchemaResponse(BaseModel):
    cust_email : str = Field(pattern=RegexPattern.EMAIL_REGEX)
    cust_checkout_date : str
    cust_checkout_time : str
    charges : float
