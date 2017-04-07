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

@application.route('/')
def index():
    return render_template('login.html')

@application.route('/logout')
def logout():

    status = request.post('<endpoint>/logout', json=request)
        
    if status == "logout":
        return render_template('login.html')
    else:
        pass

@application.route('/login', methods=['POST', 'GET'])
def login():

    # Make call to login ms
    status = request.post('<endpoint>/login', json=request)

    if status['status'] == "Success":
        email = status['email']
        token = status['token']
        currentHistory = status['currentHistory']
        return render_template('index3.html', email=email, token=token, history=currentHistory)
    else:
        pass

    return 'Invalid inputEmail/password combination'

@application.route('/register', methods=['POST', 'GET'])
def register():
    
    # Make call to register with request, get back data
    status = request.post('<endpoint>/login', json=request)

    if status['status'] == "Success":
        email = status['email']
        token = status['token']
        currentHistory = status['currentHistory']
        return render_template('index3.html', email=email, token=token, history=currentHistory)
    else:
        return render_template('login.html')

@application.route('/payment', methods=['POST', 'GET'])
def payment():

    # Make call to /payment endpoint
    status = request.post('<endpoint>/login', json=request)

    if status['status'] == "Success":
        email = status['email']
        token = status['token']
        currentHistory = status['currentHistory']
        return render_template('index3.html', email=email, token=token, history=currentHistory)
    else:
        return render_template('index3.html')

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
