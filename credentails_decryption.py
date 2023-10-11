from cryptography.fernet import Fernet  # to encrypt the username and password
from database_connection import DatabaseConnection

# using decorator
def get_encrypted_credentails(func):
    def wrapper(*args, **kwargs):
        print("Checking for credentails .... ")
        return func(*args, **kwargs)
    return wrapper

@get_encrypted_credentails
def login_into_system(user_name, password, role):
    
    try:
        with DatabaseConnection("hotel_management.db") as connection:
            cursor = connection.cursor()
            # first check is role is valid and present in table
            cursor.execute("SELECT role FROM login_credentials")
            roles = cursor.fetchall()
            # print(roles)
            for r in roles: 
                if r[0] == role.strip():
                    # print(r[0]==role)
                    break
            else:
                # print("else Executed")
                raise Exception
            cursor.execute("SELECT * FROM login_credentials WHERE role = ?", (role, ))
            record = cursor.fetchall()
            key = record[0][0]
            encrypted = record[0][2]
            fernet = Fernet(key)
            decrypted = eval(fernet.decrypt(encrypted).decode())
            return (decrypted["username"] == user_name and decrypted["password"] == password)
        
    except Exception as error:
        print(error)
        print(f"Role : {role} is not justified. Please try again!")












# """
#     code for text encryption
# """
# key = Fernet.generate_key()
# with open('utils\\filekey.key', 'wb') as filekey :
#     filekey.write(key)

# with open('utils\login_system.txt', 'rb') as file :
#     original = file.read()

# encrypted = fernet.encrypt(original)
# with open('utils\login_system.txt', 'wb') as encrypted_file :
#     encrypted_file.write(encrypted)

# code for credentails decryption

    # using file
    # with open('utils\\filekey.key', 'rb') as filekey:
    #     key = filekey.read()
    # with open('utils\\login_system.txt','rb') as encrypted_file:
    #     encrypted = encrypted_file.read()

    # # using database table creation 
    # with DatabaseConnection("hotel_management.db") as connection:
    #     cursor = connection.cursor()
    #     cursor.execute("CREATE TABLE IF NOT EXISTS login_credentials(key text, role text, credentials text)")
    #     cursor.execute("INSERT INTO login_credentials(key, role, credentials) VALUES(?, ?, ?)", (key, role, encrypted))

    # using file
    # with open('utils\\login_system.txt', 'rb') as encrypted_file:
    #     encrypted = encrypted_file.read()

    # using database table creation
    # with DatabaseConnection("login_credentails.db") as connection:
    #     cursor = connection.cursor()
    #     cursor.execute("CREATE TABLE IF NOT EXISTS credentials(encrypted_data text, role text)")
    #     cursor.execute("INSERT INTO credentials(encrypted_data, role) VALUES(?, ?)", (encrypted, role))

