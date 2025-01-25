from flask import Flask, render_template, request, redirect, flash 
import mysql.connector

app = Flask(__name__)
app.secret_key = 'root'

# Database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'electricity_db'
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Home Page
@app.route('/')
def index():
    query = "SELECT * FROM electricity_bills"
    cursor.execute(query)
    records = cursor.fetchall()
    return render_template('index.html', records=records)


# Insert Record
@app.route('/insert', methods=['GET', 'POST'])
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        # Get form data
        customer_number = request.form['customer_number']
        units_consumed = request.form['units_consumed']
        invoice_number = request.form['invoice_number']
        invoice_amount = request.form['invoice_amount']
        amount_paid = request.form['amount_paid']
        bill_date = request.form['bill_date']  # Getting the date from the form
        
        # Insert the record into the database
        query = """
            INSERT INTO electricity_bills (customer_number, units_consumed, invoice_number, invoice_amount, amount_paid, bill_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (customer_number, units_consumed, invoice_number, invoice_amount, amount_paid, bill_date))
        conn.commit()
        
        flash('Record inserted successfully!')
        return redirect('/')
    return render_template('insert.html')


# Search Record
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        customer_number = request.form['customer_number']
        query = "SELECT * FROM electricity_bills WHERE customer_number = %s"
        cursor.execute(query, (customer_number,))
        result = cursor.fetchall()
        return render_template('search.html', records=result)
    return render_template('search.html', records=None)

# Update Record
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        customer_number = request.form['customer_number']
        units_consumed = request.form['units_consumed']
        invoice_amount = request.form['invoice_amount']
        query = """UPDATE electricity_bills SET 
                   units_consumed = %s, invoice_amount = %s 
                   WHERE customer_number = %s"""
        cursor.execute(query, (units_consumed, invoice_amount, customer_number))
        conn.commit()
        flash('Record updated successfully!')
        return redirect('/')
    return render_template('update.html')

# Delete Record
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        customer_number = request.form['customer_number']
        query = "DELETE FROM electricity_bills WHERE customer_number = %s"
        cursor.execute(query, (customer_number,))
        conn.commit()
        flash('Record deleted successfully!')
        return redirect('/')
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)