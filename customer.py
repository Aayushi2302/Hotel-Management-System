# CUSTOMER MODULE
from tabulate import tabulate
import input_validation.customer_input_validation as customer_input_validation
import shortuuid
from database_connection import DatabaseConnection

class Customer:
    @classmethod
    def create_table_customer(cls):
        with DatabaseConnection("hotel_management.db") as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS customer(
                            customer_id TEXT PRIMARY KEY, 
                            name TEXT, 
                            age INTEGER, 
                            gender TEXT, 
                            email TEXT, 
                            mobile_number TEXT
                    )"""
                )

    def register_customer(self):
        try:
            self.customer_id = "C" + shortuuid.ShortUUID().random(length = 5)
            self.name = customer_input_validation.input_name()
            self.age = customer_input_validation.input_age()
            self.gender = customer_input_validation.input_gender()
            self.email = customer_input_validation.input_email_address()
            self.mobile_number = customer_input_validation.input_mobile_number()
            self.save_customer_data_to_database()
        except:
            raise Exception("Error with registration system, try again!!")
    
    def save_customer_data_to_database(self):
        with DatabaseConnection("hotel_management.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO customer(customer_id, name, age, gender, email, mobile_number) VALUES(?, ?, ?, ?, ?, ?)", 
                (self.customer_id, self.name, self.age, self.gender, self.email, self.mobile_number)
            )
        
    def print_customer_data_from_database(self):
        with DatabaseConnection("hotel_management.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM customer ORDER BY name")
            customer_data = cursor.fetchall()
            if not any(customer_data):
                print("0 records found in customer table. Please enter some records!")
                return
            row_id = [i for i in range(1,len(customer_data)+1)]
            print(
                tabulate(
                customer_data, 
                headers = ["Customer ID", "Name", "Age", "Gender", "Email Address", "Mobile Number"], 
                showindex = row_id, 
                tablefmt = "simple_grid"
                )
            )


        


