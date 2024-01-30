from pydantic import BaseModel, Field
from config.regex_pattern import RegexPattern

class LoginSchemaArguments(BaseModel):
    username : str = Field(RegexPattern.USERNAME_REGEX)
    password : str
   
class LoginSchemaResponse(BaseModel):
    access_token : str
    message : str
