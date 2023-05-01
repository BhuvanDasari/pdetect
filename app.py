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
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pdetect_user:AVB0AgbRcRl020rbg1Lfn8rkiC28WhOK@dpg-ch7g77o2qv26p1cuu9j0-a/pdetect'
#external
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pdetect_user:AVB0AgbRcRl020rbg1Lfn8rkiC28WhOK@dpg-ch7g77o2qv26p1cuu9j0-a.oregon-postgres.render.com/pdetect'
#'sqlite:///db.sqlite3'
#postgresql://user_database_cmx4_user:Yv6hGck0QJXBZgWburCYjbk5P9OCqREf@dpg-ch4nj533cv23dkld2id0-a.oregon-postgres.render.com/user_database_cmx4
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
filename = "ml/decision_tree.pickle"

class UserPassword(db.Model):
    tablename = 'username_password'
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(50))
    password_ = db.Column(db.String(50))
    patient_type_ = db.Column(db.String(50))
    

    def __init__(self, email_, password_, patient_password_):
        self.email_ = email_
        self.password_ = password_
        self.patient_type_ = patient_password_

@app.route('/')
def index():
    return "Bhuvan Chand"

@app.route('/login',methods=['POST'])
def login():

    content = request.get_json()

    email = content["email"]
    password = content["password"]
    

    user = UserPassword.query.filter_by(email).first()
    if user is None:
        return jsonify({"user":0})
    
    elif user.password == password:
        return jsonify({"user":1})
    
    else:
        return jsonify({"user":0})
    
    
@app.route('/createaccount',methods=['POST'])
def createaccount():
    content = request.get_json()

    email = content["email"]
    password = content["password"]
    confirm_password = content["password"]
    patient_type =  content["patient_type"]


    user = UserPassword.query.filter_by(email).first()
    if user is None:
        add_request = UserPassword(email_ = email, password_ = password, patient_type_ = patient_type)
        
        if password == confirm_password:
            db.session.add(add_request)
            db.session.commit()
        
        else:
            return jsonify({"user":0})
    else:
        return jsonify({"user":0})






if __name__ == '__main__':
    with app.app_context():        
        db.create_all()
    app.run(debug=True, host = "0.0.0.0")