from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_all_tables() -> list:
    connection = sqlite3.connect("database\\hotel_management.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    connection.close()
    return tables

@app.route('/')
def home():
    return render_template('home.jinja2', tables = get_all_tables())

@app.route('/table/<string:table_name>')
def table(table_name):
    
        tables = get_all_tables()
        tables = [table[0] for table in tables]
    
        connection = sqlite3.connect("database\\hotel_management.db")
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        # SELECT * FROM room; select * from customer
        data = cursor.fetchall()
        connection.close()
        return jsonify(data)

@app.route('/post/register_customer', methods=['POST', 'GET'])
def register_customer():
    if request.method == 'POST':
        cust_id = request.form.get('cust_id')
        cust_name = request.form.get('cust_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email')
        mobile_no = request.form.get('mobile_no')

        connection = sqlite3.connect("database\\hotel_management.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO customer(customer_id, name, age, gender, email, mobile_number) VALUES(?, ?, ?, ?, ?, ?)",
                       (cust_id, cust_name, age, gender, email, mobile_no))
        connection.commit()
        connection.close()
        return redirect(url_for('home'))
    
    return render_template('register_customer.jinja2')

if __name__ == '__main__':
    app.run(debug = True)