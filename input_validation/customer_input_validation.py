import re

# decorator for input validation and error handling during customer registration
def error_handling_input(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            if res == False:
                raise Exception
        except:
            print("Invalid input, enter again!!")
        finally:
            return res
    return wrapper
    
@error_handling_input
def input_validation(regular_exp, input_field) -> bool:
    r = re.fullmatch(regular_exp, input_field) 
    if r != None:
        return True
    else:
        return False

"""
    Customer class input validation
"""
def input_name() -> str:
    #  validation of name using regular expression
    while True:
        name = input("Name : ")
        check = input_validation('[A-Za-z]{2,25}\s[A-Za-z]{2,25}', name)
        if check == True:
            return name.title()

def input_age() -> int:
    # validation of age
    while True:
        try:
            age = int(input("Age : "))
            return age
        except Exception as e:
            print(e)

def input_gender() -> str:
    # validation of gender
    while True:
        try:
            gender = input("Enter F for Female and M for Male : ").capitalize()
            if gender == "F":
                return "Female"
            elif gender == "M":
                return "Male"
            else:
                raise Exception
        except:
            print("Invalid input, enter again!!")
        
def input_email_address() -> str:
    #  validation of email address using regular expression
    while True:
        email = input("Email Address : ")
        check = input_validation('^[a-z0-9]+@[a-z]+\.[a-z]{2,3}', email)
        if check == True:
           return email

def input_mobile_number() -> str:
    # validation of phone number using regular expression
    while True:
        mobile_number = input("Mobile Number : ")
        check = input_validation('[6-9][0-9]{9}', mobile_number)
        if check == True:
            return mobile_number


