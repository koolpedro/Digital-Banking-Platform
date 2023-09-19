from flask import Flask, render_template, send_from_directory, request, redirect, url_for, jsonify
from pymongo import MongoClient
from flask import session
from flask import session, abort
from flask_pymongo import PyMongo
from bson import ObjectId

import json

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.config["MONGO_URI"] = "mongodb://localhost:27017/mongodb-data"
mongo = PyMongo(app)

# Dummy user data for demonstration
user_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'address': '123 Main Street',
    'phone': '+234 0....',
    'username': 'johnEX',
    'balance': 5000.0
}

app.secret_key = '17sept2023'

# Connect to your MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mongodb-data']  # Replace with your database name
users_collection = db['users']
transactions = db['transactions']  # Define a 'transactions' collection


@app.route('/api/data')
def get_data():
    data = {'message': 'Hello from the server!'}
    return json.dumps(data)

@app.route('/static/filename')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personal')
def personal():
    return render_template('personal.html')

@app.route('/business')
def business():
    return render_template('business.html')

@app.route('/trade')
def trade():
    return render_template('trade.html')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')

@app.route('/transfer_fund')
def transfer_fund():
    return render_template('transfer_fund.html')

@app.route('/accounts')
def accounts():
    return render_template('accounts.html')

@app.route('/loan')
def loan():
    return render_template('loan.html')

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')

@app.route('/customer-profile')
def customer_profile():
    return render_template('customer_profile.html', user=user_data)

@app.route('/customer_details')
def customer_details():
     return render_template('customer_details.html')


# @app.route('/customer_details', methods=['GET', 'POST'])
# def customer_details():
#      if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']  # New line for email
#         password = request.form['password']
        
        
#         existing_user = users_collection.find_one({'username': username})
        
#         if existing_user:
#             error = 'Username already taken. Please choose another.'
#             return render_template('customer_details.html', error=error)
        
#         users_collection.insert_one({
#             'username': username,
#             'password': password,
#             'email': email  # Save the email address
#         })
#         # return redirect(url_for('login'))
        
#         return render_template('customer_details.html') 

# @app.route('/unique_customer_details', methods=['GET, POST'])
# def customer_details():
#     details = {
#         'full_name': request.form.get('full_name'),
#         'dob': request.form.get('dob'),
#         'email': request.form.get('email'),
#         'mobile_number': request.form.get('mobile_number'),
#         'occupation': request.form.get('occupation'),
#         'username': request.form.get('username'),
#         'Password': request.form.get('password'),

#         # Add other form fields here
#     }
#     mongo.db.users.insert_one(details)
#     return redirect(url_for('login'))

@app.route('/transfer-fund')
def transfer_funds():
    return render_template('transfer_fund.html')

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

@app.route('/media')
def media():
    return render_template("media.html")

@app.route('/careers')
def careers():
    return render_template("careers.html")

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({
            'username': username,
            'password': password
        })
        
        if user:
            session['username'] = user['username']  # Store username in session
            return redirect(url_for('customer_profile', username=username))
        else:
            error = 'Invalid username or password'
            return render_template("login.html", error=error)
    
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  # New line for email
        password = request.form['password']
        
        
        existing_user = users_collection.find_one({'username': username})
        
        if existing_user:
            error = 'Username already taken. Please choose another.'
            return render_template("register.html", error=error)
        
        users_collection.insert_one({
            'username': username,
            'password': password,
            'email': email  # Save the email address
        })
        return redirect(url_for('login'))
    
    return render_template("register.html")



@app.route('/profile/<username>')
def profile(username):
    if 'username' not in session:
        abort(401)  # Unauthorized
    user = users_collection.find_one({'username': username})
    
    if user:
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for('login'))
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# @app.route('/make_payment', methods=['POST'])
# def make_payment():
#     # Get data from the request
#     bank = request.form.get('bank')
#     source_account = request.form.get('source-account')
#     destination_account = request.form.get('destination-account')
#     amount = float(request.form.get('amount'))
#     description = request.form.get('description')

#     # Perform transaction processing (simplified)
#     # In a real-world application, you'd interact with a database and perform validation
#     # Here, we'll just return a success message
#     response = {
#         'message': 'Transaction successful',
#         'transaction_details': {
#             'Bank': bank,
#             'Source Account': source_account,
#             'Destination Account': destination_account,
#             'Amount': amount,
#             'Description': description,
#         }
#     }

#     return jsonify(response)

@app.route('/make_payment', methods=['POST'])
def make_payment():
    # Extract form data
    bank = request.form.get('bank')
    source_account = request.form.get('source-account')
    destination_account = request.form.get('destination-account')
    amount = float(request.form.get('amount'))
    description = request.form.get('description')

    # Create a document to insert into the MongoDB collection
    transaction_data = {
        'bank': bank,
        'source_account': source_account,
        'destination_account': destination_account,
        'amount': amount,
        'description': description
    }

    # Insert the data into the MongoDB collection
    transactions.insert_one(transaction_data)

    # Return a JSON response to the client
    response = {
        'message': 'Transaction successful',
        'transaction_details': transaction_data
    }

    return jsonify(response)

@app.route('/transaction_details/<transaction_id>')
def transaction_details(transaction_id):
    # Retrieve the transaction data by its unique ID from the MongoDB collection
    transaction_data = transactions.find_one({'_id': ObjectId(transaction_id)})
    
    # Render the 'transaction_details.html' template and pass the transaction data
    return render_template('transaction_details.html', transaction_data=transaction_data)

# transaction_list = [
#     {'_id': '1', 'bank': 'Bank 1', 'source_account': 'Account 1', 'destination_account': 'Account A', 'amount': 0.00, 'description': 'text'},
#     {'_id': '2', 'bank': 'Bank 2', 'source_account': 'Account 2', 'destination_account': 'Account B', 'amount': 0.00, 'description': 'text'},
#     # Add more transactions as needed
# ]

# @app.route('/customer_profile')
# def customer_profile():
#     return render_template('customer_profile.html', transaction_list=transaction_list)



if __name__ == '__main__':
    app.run(debug=True)
