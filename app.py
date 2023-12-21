from flask import Flask, render_template, url_for, redirect, request, session
from db import DB
from datetime import datetime as d
import random
import time
import os

app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #secret key for session

# current_dir = os.path.dirname(os.path.abspath(__file__))

# students_json = os.path.join(current_dir, 'students.json')
STUDENTDATA = DB("./students.json")

# admin_json = os.path.join(current_dir, 'admin-data.json')
ADMIN_DATA = DB("./admin-data.json")

# payment_json = os.path.join(current_dir, 'payment.json')
PAYMENT = DB("./payments.json")



def generate_transaction_id():
    timestamp = int(time.time())  # Get current timestamp
    random_num = random.randint(10000, 99999)  # Generate a random number
    transaction_id = f"TXN-{timestamp}-{random_num}"  # Create a custom ID format
    return transaction_id


@app.route('/login', methods=['POST', 'GET'])
def loginPage():

    if request.method == 'POST':
        studentid = request.form['studentid']
        matricno = request.form['matricno']

        for key, value in STUDENTDATA.read().items():
            print((key, value))
            if value['student-id'] == studentid and value['matric-no'] == matricno:
                session['userid'] = key
                return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
def index():
    if 'userid' in session:
        user_info = STUDENTDATA.read()[session['userid']]
        # user_info["userid"] = session['userid']
        return render_template('index.html', user_info=user_info)
    return redirect(url_for('loginPage'))

@app.route('/payment')
def payment():
    if 'userid' in session:
        user_info = STUDENTDATA.read()[session['userid']]
        user_info["user-id"] = session['userid']
        return render_template('checkout.html', user_info=user_info)
    return redirect(url_for('index'))

@app.route('/admin/debit/<userid>')
def adminDebit(userid):
    fee = 500
    try:
        user_info = STUDENTDATA.read()[userid]

    except KeyError:
        return "User Not Found"

    if user_info['balance'] - fee < 0:
        return "Not Enough Fund"

    user_info['balance'] -= fee
    user_info['payment-status'] = 'paid'
    admin_balance = ADMIN_DATA.read()['admin']
    admin_balance['balance'] += fee

    transaction_id = generate_transaction_id()
    now = d.now()
    time = f'{str(now.year)}-{str(now.month)}-{str(now.day)} {str(now.hour)}:{str(now.minute)}:{str(now.second)}'
    new_trans = {}
    new_trans["time"]=time
    new_trans["amount"] = fee
    new_trans["transaction-id"] = transaction_id
    new_trans["matric-no"] = user_info["matric-no"]
    new_trans["card-id"] = user_info["card-id"]
    new_trans["status"] = "paid"
    try:
        transaction_data = PAYMENT.read()
        transaction_data.append(new_trans)
        STUDENTDATA.update(userid, user_info)
        ADMIN_DATA.update('admin', admin_balance)
        PAYMENT.write(transaction_data)
        return 'Succesful'
    except:
        return 'Error in making payment'


@app.route('/sign-out')
def signOut():
    session.clear()
    return redirect(url_for('index'))


@app.route('/admin/login', methods=['POST', 'GET'])
def adminloginPage():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == 'microfinancebank@futminna.edu.ng' and password == 'futmx12345':
            session['admin-key'] = 'xyz'
            return redirect(url_for('adminPanel'))

    return render_template('admin/login.html')


@app.route('/admin')
def adminPanel():
    if 'admin-key' in session:
        admin_info = ADMIN_DATA.read()["admin"]

        # admin_info['history'] = students_info
        return render_template('admin/index.html', admin_info=admin_info)
    return redirect(url_for('adminloginPage'))


@app.route('/get-database/<history>')
def getDatabase(history):
    if history == "payment":
        payment_history = PAYMENT.read()
        return render_template('admin/payment.html', info=payment_history)
    elif history == "database":
        students_data = STUDENTDATA.read()
        students_info = []
        for value in students_data.values():
            students_info.append(value)
        return render_template('admin/database.html', database=students_info)
    else:
        return "Error In Retriving Database"

@app.route('/search-database/<history>', methods=['GET'])
def searchDatabase(history):
    q = request.args.get('q')
    answ_list = []
    if history == "payment":
        payment_history = PAYMENT.read()
        for item in payment_history:
            for value in item.values():
                if q.lower() in str(value).lower():
                    answ_list.append(item)
                    break
        return render_template('admin/payment.html', info=answ_list)
    elif history == "database":
        students_data = STUDENTDATA.read()
        for item in students_data.values():
            print(item)
            for value in item.values():
                if q.lower() in str(value).lower():
                    answ_list.append(item)
                    break
        return render_template('admin/database.html', database=answ_list)
    else:
        return "Error In Retriving Database"



@app.route('/verify-transaction/<userid>', methods=['POST'])
def verifyTransaction(userid):
    if request.method == "POST":
        amount = request.form["amount"]

        user_info = STUDENTDATA.read()[userid]
        user_info['balance'] += int(amount)
        STUDENTDATA.update(userid, user_info)
        return 'ok'






