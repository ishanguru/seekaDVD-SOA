from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import stripe
import jwt
from datetime import datetime

from flask_cors import CORS, cross_origin

STRIPE_PUBLISHABLE_KEY = 'pk_test_PdLFWUk0BeVmaCrviRaoKxjN'
STRIPE_SECRET_KEY = 'sk_test_ALv9duL6BrcdpUv7U20KGr99'

stripe.api_key = STRIPE_SECRET_KEY
stripe.api_base = "https://api-tls12.stripe.com"

application = Flask(__name__,template_folder='templates')

CORS(application)

application.config['MONGO_DBNAME'] = 'userdb'
application.config['MONGO_URI'] = 'mongodb://Gunnernet:nachiket_99@ds147069.mlab.com:47069/userdb'
application.secret_key = 'newsecret'

mongo = PyMongo(application)

tokentoken = None

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

@application.route('/payment', methods=['POST', 'GET'])
def payment():

    data = {}
    jwtToken = request.form['jwtToken']
    tokentoken = request.form['jwtToken']
    currentUser = request.form['stripeEmail']

    try:
        tokend = jwt.decode(jwtToken, application.config.get('SECRET_KEY'), algorithm= 'HS256')
    except Exception as e:
        print e
        return render_template('login.html')

    cartTotal = float(request.form['cartTotal'])

    token = request.form['stripeToken']
    amount = cartTotal*100

    print("Charging Customer")
    charge = stripe.Charge.create(
        amount=amount,
        currency='usd',
        description='A payment for seeka-dvd',
        source=token
    )
    print(charge)

    userhistory = mongo.db.userhistory
    now = str(datetime.date(datetime.now()))

    userhistory.insert_one({"name": currentUser, "TransactionAmount": cartTotal, "TransactionTime": now})
    currentHistory = list(userhistory.find({"name" : currentUser}))

    data['status'] = "Success"
    data['email'] = email
    data['token'] = token
    data['currentHistory'] = currentHistory

    return jsonify(data)

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
