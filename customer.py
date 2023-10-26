"""
    This is a customer module of the Hotel Reservation System project.
    This module is contains a Customer class which has method to handle following functionalities :
    1. Registering of customer
    2. Saving Customer details to database
    3. Printing Customer details
    4. Remove Customer
"""

# third party imports
from tabulate import tabulate
import shortuuid

# local file imports
import input_validation.customer_input_validation as customer_input_validation
import database.database_helper as database_helper
from database.query_collector import CustomerQuery

class Customer:
    def register_customer(self) -> None:
        try:
            print("Enter customer details....\n")
            self.customer_id = "C" + shortuuid.ShortUUID().random(length = 5)
            self.name = customer_input_validation.input_name()
            self.age = customer_input_validation.input_age()
            self.gender = customer_input_validation.input_gender()
            self.email = customer_input_validation.input_email_address()
            self.mobile_number = customer_input_validation.input_mobile_number()
            self.save_customer_data_to_database()
        except:
            raise Exception("Error with registration system, try again!!")
    
    def save_customer_data_to_database(self) -> None:
        query = CustomerQuery.QUERY_FOR_SAVING_CUSTOMER_DATA
        data = (self.customer_id, self.name, self.age, self.gender, self.email, self.mobile_number)
        database_helper.update_database(query, data)   
        
    def print_customer_data_from_database(self) -> None:
        query = CustomerQuery.QUERY_FOR_FETCHING_CUSTOMER_DATA
        customer_data = database_helper.fetch_data_from_database(query)
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

    def remove_customer_data_from_database(self) -> None:
        # add the check for user 
        customer_email = customer_input_validation.input_email_address()
        query_for_customer_id = CustomerQuery.QUERY_FOR_FETCHING_CUSTOMER_ID_WITH_EMAIL
        customer_id_for_deletion = database_helper.fetch_data_from_database(query_for_customer_id, (customer_email,))
        # print(customer_id_for_deletion)
        if not any(customer_id_for_deletion):
            print(f"{customer_email} does not exist!")
            return
        else:
            query = CustomerQuery.QUERY_FOR_REMOVING_CUSTOMER_DATA
            data = (customer_id_for_deletion[0][0], ) 
            database_helper.update_database(query, data)
            print("Data deleted successfully!")


