import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from scipy.signal import butter, filtfilt, correlate, periodogram
import datetime
import pickle
#from sklearn.preprocessing import LabelEncoder
import math
app = Flask(__name__)
#localhost
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

#internal
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pdetect_user:AVB0AgbRcRl020rbg1Lfn8rkiC28WhOK@dpg-ch7g77o2qv26p1cuu9j0-a/pdetect'

#external
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pdetect_user:AVB0AgbRcRl020rbg1Lfn8rkiC28WhOK@dpg-ch7g77o2qv26p1cuu9j0-a.oregon-postgres.render.com/pdetect'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
filename = "ml/decision_tree.pickle"

class UserPassword(db.Model):
    tablename = 'username_password'
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(50))
    password_ = db.Column(db.String(50))
    patient_type_ = db.Column(db.String(50))
    

    def __init__(self, email_, password_, patient_type_):
        self.email_ = email_
        self.password_ = password_
        self.patient_type_ = patient_type_

@app.route('/')
def index():
    return "Bhuvan Chand"

@app.route('/login',methods=['POST'])
def login():

    content = request.get_json()

    email = content["email"]
    password = content["password"]
    print(email)

    user = UserPassword.query.filter_by(email_= email).first()
    if user is None:
        return jsonify({"user":0})
    
    elif user.password_ == password:
        return jsonify({"user":1})
    
    else:
        return jsonify({"user":0})
    
    
@app.route('/createaccount',methods=['POST'])
def createaccount():
    content = request.get_json()

    email = content["email"]
    password = content["password"]
    confirm_password = content["confirm_password"]
    patient_type =  content["patient_type"]


    user = UserPassword.query.filter_by(email_ = email).first()
    if user is None and password == confirm_password:
        add_request = UserPassword(email_ = email, password_ = password, patient_type_ = patient_type)
        db.session.add(add_request)
        db.session.commit()

        return jsonify({"user":1})

    elif user is None and password != confirm_password: 
        return jsonify({"user":2})

    else:
        return jsonify({"user":0})






if __name__ == '__main__':
    with app.app_context():        
        db.create_all()
    app.run(debug=True, host = "0.0.0.0")
