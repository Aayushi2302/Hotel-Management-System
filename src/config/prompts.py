class Prompts:

    # common
    INVALID_INPUT = "Invalid input... Try again"
    ENTER_CHOICE = "Enter your choice: "
    SUCCESSFUL_LOGOUT = "Logout successful..."

    # main
    WELCOME_MESSAGE = "----- Welcome to Hotel Reservation System ------"
    EXIT_MESSAGE = "----- Thank you for using Hotel Reservation System ------"
    ZERO_RECORD = "0 record found in {} table. Please enter some records."

    # auth views
    ADMIN_NOT_FOUND = "Admin not registered. Please register admin..."
    INPUT_NAME = "Enter name: "
    USERNAME_FORMAT = "Username should be in the format user@ followed by atleast 5 characters"
    INPUT_USERNAME = "Enter username: "
    INPUT_EMPLOYEE_AGE = "Enter age: "
    INPUT_EMPLOYEE_GENDER = "Enter gender: "
    INPUT_EMPLOYEE_ROLE = "Enter role: "
    INPUT_PASSWORD = "Enter password: "
    INPUT_ROOM_ID = "Enter room id: "
    CUSTOMER_OUT_DATE_INPUT = "Enter expected out date: "
    CUSTOMER_OUT_TIME_INPUT = "Enter expected out time: "
    CANNOT_INPUT_PAST_DATE_TIME = "Your entered a date and time that has either already passed or is invalid. Please enter again..."
    CANNOT_CREATE_ADMIN = "Admin cannot be created again...Enter some other role"
    INPUT_EMPLOYEE_EMAIL = "Enter email: "
    INPUT_MOBILE_NUMBER = "Enter mobile number: "
    SUCCESSFUL_CREDENTIAL_CREATION = "Credentials created successfully..."
    UNSUCCESSFUL_CREDENTIAL_CREATION = "Unable to create credentials..."
    LOGIN_ATTEMPTS_EXHAUSTED = "Login attempts exhausted! Please login after some time..."
    INPUT_CREDENTIAL = "Enter your credentials: "
    CHANGE_PASSWORD = "Update your password..."
    STRONG_PASSWORD_REQUIREMENTS = "Please enter a password following below requirements:\nPassword length should be 8 characters or more with atleast one uppercase, one lowercase letter, one digit and one special symbol like @, #, $, %, &"
    INPUT_NEW_PASSWORD = "New Password : "
    WEAK_PASSWORD_INPUT = "You entered a weak password...Please follow mentioned instructions to create a strong password"
    INPUT_CONFIRM_PASSWORD = "Confirm Password : "
    PASSWORD_NOT_MATCH = "Password does not match. Please enter your password again!"
    PASSWORD_CHANGE_SUCCESSFUL = "Password changed successfully! Now login with your new password..."
    EXIT_SYSTEM = "Do you want to exit from the system (Y/N)?"
    LOGIN_ATTEMPTS_LEFT = "Invalid login...\nLogin attempts left : {}"
    INPUT_TIME_IN_24_HOUR_FORMAT = "Input time in 24 hour format"

    # customer views
    ENTER_CUSTOMER_DETAILS = "Enter customer details....\n"
    SUCESSFUL_CUSTOMER_CREATION = "Customer details saved successfully..."
    UNSUCCESSFUL_CUSTOMER_CREATION = "Unable to create customer..."
    CUSTOMER_DOES_NOT_EXIST = "Customer does not exist..."
    SUCCESSFUL_CUSTOMER_REMOVAL = "Customer removed successfully..."
    UNSUCCESSFUL_CUSTOMER_REMOVAL = "Unable to remove customer..."

    # room views
    ENTER_ROOM_DETAILS = "Enter room details....\n"
    SUCCESSFUL_ROOM_CREATION = "Room registered successfully...."
    UNSUCCESSFUL_ROOM_CREATION = "Unable to register room..."
    ROOM_DOES_NOT_EXIST = "Given room does not exist..."
    ROOM_ALREADY_INACTIVE = "Given room is already inactive..."
    SUCCESSFUL_ROOM_DEACTIVATION = "Room deactivated successfully..."
    UNSUCCESSFUL_ROOM_DEACTIVATION = "Unable to deactivate room..."
    ROOM_ALREADY_ACTIVE = "Given room is already active..."
    SUCCESSFUL_ROOM_ACTIVATION = "Room activated successfully..."
    UNSUCCESSFUL_ROOM_ACTIVATION = "Unable to activate room..."
    PREFERRED_ROOM_NOT_EXIST = "Sorry room does not exist according to your preference..."
    INPUT_RESERVE_OTHER_ROOM = "Do you want to reserve any other room available(y/n) ?"
    NO_ROOMS_AVAILABLE = "Sorry no rooms are available..."
    UNSUCCESSFUL_CHECK_IN = "Unable to check in..."
    SUCCESSFUL_CHECK_IN = "Checked in the room successfully..."
    UNSUCCESSFUL_CHECK_OUT = "Unable to check out..."
    SUCCESSFUL_CHECK_OUT = "Checked out the room successfully..."


    # error handler
    INTEGRITY_ERROR_MESSAGE = "You entered data that already exist. Please enter unique data"
    OPERATIONAL_ERROR_MESSAGE = "Something unexpected happened with the Database. Please try again after some time"
    PROGRAMMING_ERROR_MESSAGE = "Something wrong with the code on backend. Please wait while we resolve the issue"
    GENERAL_EXCEPTION_MESSAGE = "We are encountering some issue with the system.\nWe will be back soon.\nThank you for waiting..."
    
    # menu prompts
    STAFF_OR_RECEPTION_MENU = """
    Welcome to staff module :-)

    You can perfrom the below tasks :
    1. Register a customer
    2. Check in
    3. Check out
    4. Print room details
    5. Print customer details
    6. Logout
    """

    ADMIN_MENU = """
    Welcome to admin module :-)

    You can perfrom the below tasks :
    1. Add room
    2. Activate room
    3. Deactivate room
    4. Print room details
    5. Add login credentials
    6. Logout
    """
    
   

    