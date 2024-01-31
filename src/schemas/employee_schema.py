from pydantic import BaseModel, Field
from config.regex_pattern import RegexPattern

class EmployeeSchemaResponse(BaseModel):
    employee_id : str
    username : str = Field(pattern=RegexPattern.USERNAME_REGEX)
    password : str
    role : str = Field(pattern=RegexPattern.ROLE_REGEX)
    password_type : str

class EmployeeSchemaArguments(BaseModel):
    username : str = Field(pattern=RegexPattern.USERNAME_REGEX)
    role : str = Field(pattern=RegexPattern.ROLE_REGEX)