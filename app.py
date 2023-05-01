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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

#internal
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pdetect_user:AVB0AgbRcRl020rbg1Lfn8rkiC28WhOK@dpg-ch7g77o2qv26p1cuu9j0-a/pdetect'

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
    user_type_ = db.Column(db.String(50))

    


    

    def __init__(self, email_, password_, user_type_):
        self.email_ = email_
        self.password_ = password_
        self.user_type_ = user_type_
        

class UserDetails(db.Model):
    tablename = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    height = db.Column(db.Float)
    bmi = db.Column(db.Float)
    heartrate = db.Column(db.Integer)
    arthype = db.Column(db.String(50))
    subhypo = db.Column(db.String(50))
    dia = db.Column(db.String(50))
    ldopa = db.Column(db.Integer)
    orthohypo = db.Column(db.String(50))
    basetemp = db.Column(db.Float)
    handtemp = db.Column(db.Float)
    thirdfingtemp = db.Column(db.Float)
    rr = db.Column(db.Float)



    

    def __init__(self, name,age,gender,weight,height,ldopa,rr,
                 bmi,basetemp,handtemp,thirdfingertemp,dia,arthype,heartrate,
                 subhypo,orthohypo):
        self.name = name
        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.bmi = bmi
        self.heartrate = heartrate
        self.arthype = arthype
        self.subhypo = subhypo
        self.dia = dia
        self.ldopa = ldopa
        self.orthohypo = orthohypo
        self.basetemp = basetemp
        self.handtemp = handtemp
        self.thirdfingertemp = thirdfingertemp
        self.rr = rr
        

@app.route('/')
def index():
    return "Bhuvan Chand"

@app.route('/login',methods=['POST'])
def login():

    content = request.get_json()

    email = content["email"]
    password = content["password"]
    

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
    user_type =  content["user_type"]


    user = UserPassword.query.filter_by(email_ = email).first()
    if user is None and password == confirm_password:
        add_request = UserPassword(email_ = email, password_ = password, user_type_ = user_type)
        db.session.add(add_request)
        db.session.commit()

        return jsonify({"user":1})

    elif user is None and password != confirm_password: 
        return jsonify({"user":2})

    else:
        return jsonify({"user":0})
    

@app.route('/viewuserdetails',methods=['POST'])
def viewuserdetails():
    

    user = UserDetails.query.filter_by(id = 1).first()
    

    if user is None:
        return jsonify({"name":"", "age":"",
                    "gender":"", "ldopa":"",
                    "bmi":"", "rr":"", "basetemp":"",
                    "thirdfingtemp":"",
                    "handtemp":"", "dia":"",
                    "height":"", "weight":"", 
                    "heartrate":"","orthohypo":"",
                    "subhypo":"","arthype":""})
    
    else:
        return jsonify({"name":user.name, "age":user.age,
                        "gender":user.gender, "ldopa":user.ldopa,
                        "bmi":user.bmi, "rr":user.rr, "basetemp":user.basetemp,
                        "thirdfingtemp":user.thirdfingtemp,
                        "handtemp":user.handtemp, "dia":user.dia,
                        "height":user.height, "weight":user.weight, 
                        "heartrate":user.heartrate,"orthohypo":user.orthohypo,
                        "subhypo":user.subhypo,"arthype":user.arthype})


@app.route('/edituserdetails',methods=['POST'])
def edituserdetails():
    content = request.get_json()

    name = content['name']
    age = content['age']
    gender = content['gender']
    ldopa = content['ldopa']
    bmi = content['bmi']
    rr = content['rr']
    basetemp = content['basetemp']
    handtemp = content['handtemp']
    thirdfingtemp = content['thirdfingtemp']
    dia = content['dia']
    height = content['height']
    weight = content['weight']
    heartrate = content['heartrate']
    orthohypo = content['orthohypo']
    subhypo = content['subhypo']
    arthype = content['arthype']


    user = UserDetails.query.filter_by(id = 1).first()

    if user is None:
        user_add_request = UserDetails(name = name, 
                  age = age,
                  gender = gender,ldopa = ldopa,
                  bmi = bmi,rr = rr,
                  basetemp = basetemp,handtemp = handtemp,
                  thirdfingertemp = thirdfingtemp,dia = dia,
                  height = height,weight = weight,
                  heartrate = heartrate,orthohypo = orthohypo,
                  subhypo = subhypo,arthype = arthype)
        db.session.add(user_add_request)
        db.session.commit()

    else:
        user.name = name
        user.age = age
        user.gender = gender
        user.ldopa = ldopa
        user.bmi = bmi
        user.rr = rr
        user.basetemp = basetemp
        user.thirdfingtemp = thirdfingtemp
        user.handtemp = handtemp
        user.dia = dia
        user.height = height
        user.weight = weight
        user.heartrate = heartrate
        user.orthohypo = orthohypo
        user.subhypo = subhypo
        user.arthype = arthype

        db.session.commit()

    return jsonify({})








if __name__ == '__main__':
    with app.app_context():        
        db.create_all()
    app.run(debug=True, host = "0.0.0.0")
