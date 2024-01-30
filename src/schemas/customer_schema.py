from pydantic import BaseModel, Field
from config.regex_pattern import RegexPattern

class CustomerSchemaResponse(BaseModel):
    cust_id : str
    name : str = Field(pattern=RegexPattern.NAME_REGEX)
    age : int = Field(gt=15, lt=60)
    gender : str
    email : str = Field(pattern=RegexPattern.EMAIL_REGEX)
    mobile_number : str = Field(pattern=RegexPattern.MOBILE_NO_REGEX)
    status : str

class CustomerSchemaArguments(BaseModel):
    name : str = Field(pattern=RegexPattern.NAME_REGEX)
    age : int = Field(gt=15, lt=60)
    gender : str
    email : str = Field(pattern=RegexPattern.EMAIL_REGEX)
    mobile_number : str = Field(pattern=RegexPattern.MOBILE_NO_REGEX)

class CustomerUpdateSchema(BaseModel):
    cust_email : str = Field(pattern=RegexPattern.EMAIL_REGEX)
    status : str
